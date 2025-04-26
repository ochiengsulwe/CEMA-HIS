"""
This module defines how a single is appointment is retrieved for adults only.
"""
from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.appointment import Appointment
from models.loginfo import LogInfo


def one_appointment(appointment_id):
    """
        Retrieves a single appointment for the associated authenticated user.

        Args:
            appointment_id (str): The ID of the appointment to retrieve.

        Returns:
           tuple: response containing a list of appointments or an error message.
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        appointment = storage.get(Appointment, appointment_id)
        if not appointment:
            return jsonify({'error': 'appointment not found'}), 404

        if appointment not in user.adult_profile.appointments:
            return jsonify({'error': 'not authorised'}), 403
        if user.account_type == 'adult':
            name_ = appointment.practitioner.identity
        else:
            return jsonify({'error': 'not authorised'}), 403

        first_name = name_.first_name
        middle_name = name_.middle_name
        last_name = name_.last_name

        name = " ".join(filter(None, [first_name, middle_name, last_name]))

        appointments_by_name = defaultdict(list)
        for schedule in getattr(appointment, 'schedules', []):
            appointment_details = {
                "date": schedule.date.strftime('%Y-%m-%d'),
                "start_time": schedule.time_from.strftime("%H:%M"),
                "end_time": schedule.time_to.strftime("%H:%M"),
                "appointment_status": schedule.appointment.status,
                "appointment_type": schedule.appointment.type,
                "appointment_state": schedule.status,
                "schedule_id": schedule.id
            }
            appointments_by_name[name].append(appointment_details)

        return jsonify(dict(appointments_by_name)), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
