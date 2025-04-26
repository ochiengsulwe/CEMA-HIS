"""The module describes appointment cancellation.

    This actually means deleting the appointment schedules(the appointed times) if
        the appointment is a reccurent one, or deleting the whole appointment entry
        if the appointment was to occur just once.
    If the appointment is recurrent, only the awaiting appointments are to be deleted.
    This DELETES ALL other incompleted appointments/schedules

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
from models.appointment import Appointment
from models.loginfo import LogInfo
from utils.create_planner import create_planner


def end_appointment(appointment_id):
    """
    Deletes a list of appointment  schedules from the database.

    If the appointment type is once, then the whole appointment entry plus the
        associated schedule is deleted. If the appointment is of type repeat, then only
        the specific schedule is deleted.

    Args:
        appointment_id (str): the actual appointment to be deleted.
        schedule_id (:obj: `str: optional): only required if the appointment type is
            repeat so as to get the exact appointment schedule to remove.

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

        if user_.account_type == 'practitioner':
            user = user_.prac_profile
        else:
            return jsonify({'error': 'not authorised'}), 403

        appointment = storage.get(Appointment, appointment_id)
        if not appointment:
            return jsonify({'error': 'appointment not found'}), 404

        if appointment not in user.appointments:
            return jsonify({'error': 'not authorised'}), 403

        freed_slots = []

        if (appointment.type == 'once'):
            if (len(appointment.schedules) == 1 and
                    appointment.schedules[0].status == 'pending'):
                freed_slots.append({
                    "date": appointment.schedules[0].date,
                    "time_from": appointment.schedules[0].time_from,
                    "time_to": appointment.schedules[0].time_to
                })
                appointment.delete()
                storage.save()
                message = "appointment successfully closed"

            elif (len(appointment.schedules) == 1 and
                  appointment.schedules[0] == 'complete'):
                return jsonify({'error': 'can not close this appointment'}), 403
            else:
                return jsonify({'error': 'not authorised'}), 403

        elif (appointment.type == 'repeat'):
            for s in appointment.schedules:
                if s.status == 'pending':
                    freed_slots.append({
                        "date": s.date,
                        "time_from": s.time_from,
                        "time_to": s.time_to
                    })
                    s.delete()
                    storage.save()
            message = "appointment successfully closed"
        else:
            return jsonify({'error': 'not authorised'}), 403

        # Restore freed-up slots in the practitioner's planner
        for freed_slot in freed_slots:
            date = freed_slot['date']
            time_from = freed_slot['time_from']
            time_to = freed_slot['time_to']
            prac_id = user.id
            create_planner(db.session, prac_id, date, time_from, time_to)

        return jsonify({'message': message}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
