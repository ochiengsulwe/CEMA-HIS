"""The module describes appointment cancellation.

    This actually means deleting the appointent schedule(the appointed times) if
        the appointment is a reccurent one, or deleting the whole appointment entry
        if the appointment was to occur just once.
    If the appointment is recurrent, only the awaiting appointments are to be deleted.

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
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.schedule import Schedule
from utils.create_planner import create_planner


def cancel_appointment(schedule_id):
    """
    Deletes an appointment schedule from the database.

    If the appointment type is once, then the whole appointment entry plus the
        associated schedule is deleted. If the appointment is of type repeat, then only
        the specific schedule is deleted.

    Args:
        schedule_id (str): unique schedule identifier

    Returns:
        tuple: A success or error message, coupled with the respective HTTPS response
            code.
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'error': 'not authorised'}), 401

    try:
        user_ = storage.get(LogInfo, current_user_id)

        if not user_:
            return jsonify({'error': 'user not found'}), 404

        if user_.account_type == 'adult':
            user = user_.adult_profile
        else:
            return jsonify({'error': 'not authorised'}), 403

        schedule = storage.get(Schedule, schedule_id)
        if not schedule:
            return jsonify({'error': 'appointment schedule not found'}), 404

        appointment = schedule.appointment
        if not appointment:
            return jsonify({'error': 'appointment not found'}), 404

        if appointment not in user.appointments:
            return jsonify({'error': 'not authorised'}), 403

        prac = appointment.practitioner
        if not prac:
            return jsonify({'error': 'practitioner not found'}), 404

        freed_slot = {}

        if (appointment.type == 'once' and appointment in user.appointments):
            if (len(appointment.schedules) == 1 and
                    appointment.schedules[0].status == 'pending'):
                freed_slot.update({
                    "date": appointment.schedules[0].date,
                    "time_from": appointment.schedules[0].time_from,
                    "time_to": appointment.schedules[0].time_to
                })
                appointment.delete()
                storage.save()
                message = "appointment successfully deleted"

            elif (len(appointment.schedules) == 1 and
                  appointment.schedules[0] == 'complete'):
                return jsonify({'error': 'can not delete this appointment'}), 403
            else:
                return jsonify({'error': 'not authorised'}), 403

        elif (appointment.type == 'repeat' and schedule_id and appointment in
                user.appointments):
            if (schedule.status == 'complete' or schedule not in
                    appointment.schedules):
                return jsonify({'error': 'not authorised'}), 403
            if schedule.status == 'pending' and schedule in appointment.schedules:
                freed_slot.update({
                    "date": schedule.date,
                    "time_from": schedule.time_from,
                    "time_to": schedule.time_to
                })
                schedule.delete()
                storage.save()
                message = "schedule successfully deleted"
        else:
            return jsonify({'error': 'not authorised'}), 403

        if freed_slot:
            date = freed_slot['date']
            time_from = freed_slot['time_from']
            time_to = freed_slot['time_to']
            prac_id = prac.id
            create_planner(db.session, prac_id, date, time_from, time_to)

        return jsonify({'message': message}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
