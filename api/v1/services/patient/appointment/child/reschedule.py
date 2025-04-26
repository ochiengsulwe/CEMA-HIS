"""The module describes appointment rescheduling.

    This actually means changing the appointent schedule(the appointed times).
    If the appointment is recurrent, only the awaiting appointments are to be
        rescheduled.

    Every `Appointment` class model is attached to a `Schedule` class models to
        track its recurrence:
            Example:
                appointment = Appointment()
                schedule = Schedule()
                appointment.schedules.append(schedule)

                if len(appointment.schedules) == 1:
                    then the appointment is of type `once`
                if len(appointment.schedules) > 1:
                    then the appointment is of type `recurrent`
                NOTE: len(appointment.schedules) should never be less than 1.
"""
from datetime import datetime
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.child_profile import ChildProfile
from models.loginfo import LogInfo
from models.schedule import Schedule
from models.practitioner_profile import PracProfile

from utils.adjust_free_time import adjust_planner
from utils.create_planner import create_planner
from utils.database import record_integrity
from utils.general import data_check
from utils.overlap import schedule_overlap, span_find
from utils.support import is_parent


def reschedule_appointment(data, child_id, schedule_id):
    """
    Reschedules an appointment by updating a specific schedule times and/or date.

    Args:
        child_id (str): child's profile ID
        schedule_id (str): only required if the appointment type is
            repeat so as to get the exact appointment schedule to remove.
        data(dict): new appointment details containing time_from, time_to  and/or date

    Returns:
        tuple: A success or error message, coupled with the respective HTTPS response
            code.
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'error': 'not signed in'}), 401

    required_fields = ['date', 'time_from', 'time_to']
    if not data:
        return jsonify({'error': 'not json'}), 400

    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    time_from = datetime.strptime(data['time_from'], '%H:%M').time()
    time_to = datetime.strptime(data['time_to'], '%H:%M').time()

    error_response = data_check(data, required_fields)
    if error_response:
        return error_response

    try:
        user_ = storage.get(LogInfo, current_user_id)
        if not user_:
            return jsonify({'error': 'user not found'}), 404

        child = storage.get(ChildProfile, child_id)
        if not child:
            return jsonify({'error': 'child not found'}), 404

        if user_.account_type == 'adult':
            return jsonify({'error': 'not authorised'}), 403

        if not is_parent(child, user_):
            return jsonify({'error': 'not authorised'}), 403

        schedule = storage.get(Schedule, schedule_id)
        if not schedule:
            return jsonify({'error': 'appointment schedule not found'}), 404

        if schedule.appointment not in child.appointments:
            return jsonify({'error': 'not authorised'}), 403

        pr = schedule.appointment.practitioner.id
        prac = storage.get(PracProfile, pr)
        if not prac:
            return jsonify({'error': 'practitioner was not found'}), 404
        # check for overlaps in other appointments for both prac and patient
        appointment = schedule.appointment
        overlap = (
            schedule_overlap(appointment.practitioner, date, time_from, time_to) or
            schedule_overlap(appointment.child_profile, date, time_from, time_to)
        )
        if overlap:
            return jsonify({'error': 'have another appointment at this time.'}), 409

        # check if practitioner is free at this time
        free = span_find(appointment.practitioner, date, time_from, time_to)
        if not free:
            return jsonify({'error', 'no free time available at this time'})

        freed_slot = {}
        if (appointment.type == 'once'):
            if (len(appointment.schedules) == 1 and
                    appointment.schedules[0].status == 'pending'):
                freed_slot.update({
                    "date": appointment.schedules[0].date,
                    "time_from": appointment.schedules[0].time_from,
                    "time_to": appointment.schedules[0].time_to
                })
                status = appointment.schedules[0].status

                appointment.schedules[0].delete()
                storage.save()

                # Create the newly updated schedule entry
                schedule = record_integrity(db.session, Schedule,
                                            time_from=time_from,
                                            time_to=time_to,
                                            date=date,
                                            status=status,
                                            appointment=appointment
                                            )
                schedule.save()

                message = "appointment successfully rescheduled"

            elif (len(appointment.schedules) == 1 or
                  appointment.schedules[0] == 'complete'):
                return jsonify({'error': 'can not reschedule this appointment'}), 403
            else:
                return jsonify({'error': 'not authorised'}), 403

        elif (appointment.type == 'repeat' and schedule_id):
            schedule = storage.get(Schedule, schedule_id)
            if not schedule:
                return jsonify({'error': 'schedule not found'}), 404
            if (schedule.status == 'complete' or schedule not in
                    appointment.schedules):
                return jsonify({'error': 'not authorised'}), 403
            if schedule.status == 'pending' and schedule in appointment.schedules:
                freed_slot.update({
                    "date": schedule.date,
                    "time_from": schedule.time_from,
                    "time_to": schedule.time_to
                    })
                status = schedule.status

                schedule.delete()
                storage.save()

                # Create a new schedule entry
                schedule = record_integrity(db.session, Schedule,
                                            time_from=time_from,
                                            time_to=time_to,
                                            date=date,
                                            status=status,
                                            appointment=appointment
                                            )
                schedule.save()

                message = "schedule successfully updated"
        else:
            return jsonify({'error': 'not authorised'}), 403

        # yunking appointment time from prac's span above(free)
        adjust_planner(free, time_from, time_to)
        storage.save()

        # Restore freed-up slots in the practitioner's planner
        if freed_slot:
            date = freed_slot.get('date')
            time_from = freed_slot.get('time_from')
            time_to = freed_slot.get('time_to')
            create_planner(db.session, pr, date, time_from, time_to)
        return jsonify({'message': message}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
