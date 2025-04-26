"""
This module defines how all upcoming appointments will be retrieved for practitioners
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


def pending_appointments():
    """
        Retrieves all upcoming appointments for the authenticated practitioner.

        Returns:
            tuple: response containing a list of appointments or an error message.
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'mesasge': 'user not found'}), 404

        if user.account_type == 'practitioner':
            appointments = user.prac_profile.appointments
        else:
            return jsonify({'error': 'not authorised'}), 403

        # Fetch all schedules related to the appointments
        schedules = Schedule.query.filter(
            and_(
                Schedule.appointment_id.in_([a.id for a in appointments]),
                Schedule.status == 'pending'
            )
        ).all()

        # Group schedules by date
        appointments_by_date = defaultdict(list)
        for schedule in schedules:
            appointment = schedule.appointment

            if user.account_type == 'practitioner':
                if appointment.adult_profile is not None:
                    name_ = appointment.adult_profile.identity
                elif appointment.child_profile is not None:
                    name_ = appointment.child_profile.identity
                else:
                    return jsonify({'error': 'not authorised'}), 403

            first_name = name_.first_name
            middle_name = name_.middle_name
            last_name = name_.last_name
            name = " ".join(filter(None, [first_name, middle_name, last_name]))

            # Build appointment details
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
