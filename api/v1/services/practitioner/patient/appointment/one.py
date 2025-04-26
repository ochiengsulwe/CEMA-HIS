"""
This module defines how one patient appointment relating to the practitioner will
    be retrieved
"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.schedule import Schedule


def patient_appointment(schedule_id):
    """
        Retrieves one related patient appointments for the authenticated practitioner.

        Args:
            schedule_id (str): appointment schedule's unique identifier

        Returns:
            tuple: response containing a appointment schedule info or an error message.
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'mesasge': 'user not found'}), 404

        schedule = storage.get(Schedule, schedule_id)
        if not schedule:
            return jsonify({'error': 'schedule not found'})

        if schedule.appointment.adult_profile is not None:
            profile = schedule.appointment.adult_profile
            identity = profile.identity
        elif schedule.appointment.child_profile is not None:
            profile = schedule.appointment.child_profile
            identity = profile.identity

        if user.account_type != 'practitioner':
            return jsonify({'error': 'not authorised'}), 403

        prac = user.prac_profile
        if not prac:
            return jsonify({'error': 'practitioner account does not exist'}), 404

        if (
            schedule.appointment not in prac.appointments or schedule.appointment not in
                profile.appointments
        ):
            return jsonify({'error': 'not authorised'}), 403

        first_name = identity.first_name
        middle_name = identity.middle_name
        last_name = identity.last_name
        name = " ".join(filter(None, [first_name, middle_name, last_name]))

        appointment_details = {
            "start_time": schedule.time_from.strftime("%H:%M"),
            "end_time": schedule.time_to.strftime("%H:%M"),
            "appointment_status": schedule.appointment.status,
            "appointment_type": schedule.appointment.type,
            "appointment_state": schedule.status,
            "appointment_with": name,
            "appointment_schedule_id": schedule.id,
            "appointment_id": schedule.appointment.id,
            "day_of_week": schedule.date.strftime('%A'),
            "date": schedule.date.strftime('%Y-%m-%d')
        }

        return jsonify(appointment_details), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
