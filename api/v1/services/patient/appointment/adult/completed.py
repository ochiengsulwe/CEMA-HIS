"""
This module defines how completed appointments will be retrieved for adults only.

"""
from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.schedule import Schedule


def completed_appointments():
    """
        Retrieves all completed appointments for the authenticated adult user.

        Returns:
            tuple: response containing a list of appointments or an error message, and
                associated HTTP repsonse code
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        if user.account_type == 'adult':
            appointments = user.adult_profile.appointments
        else:
            return jsonify({'error': 'not authorised'}), 403

        schedules = Schedule.query.filter(
            and_(
                Schedule.appointment_id.in_([a.id for a in appointments]),
                Schedule.status == 'complete'
            )
        ).all()

        appointments_by_date = defaultdict(list)
        for schedule in schedules:
            appointment = schedule.appointment

            if user.account_type == 'adult':
                name_ = appointment.practitioner.identity
            else:
                return jsonify({'error': 'not authorised'}), 403

            first_name = name_.first_name
            middle_name = name_.middle_name
            last_name = name_.last_name
            name = " ".join(filter(None, [first_name, middle_name, last_name]))

            appointment_details = {
                "start_time": schedule.time_from.strftime("%H:%M"),
                "end_time": schedule.time_to.strftime("%H:%M"),
                "appointment_status": schedule.appointment.status,
                "appointment_type": schedule.appointment.type,
                "appointment_state": schedule.status,
                "appointment_with": name,
                "appointment_id": schedule.appointment.id
            }
            appointments_by_date[schedule.date.strftime('%Y-%m-%d')].append(
                appointment_details)

        return jsonify(appointments_by_date), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
