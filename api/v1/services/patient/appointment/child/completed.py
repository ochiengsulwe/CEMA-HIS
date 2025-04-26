"""
This module defines how all completed appointments will be retrieved for dependents.
"""
from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.child_profile import ChildProfile
from models.loginfo import LogInfo
from models.schedule import Schedule
from utils.support import is_parent


def completed_appointments(child_id):
    """
        Retrieves all completed appointments for a child via an authenticated
            parent's account.

        Args:
            child_id (str): A child's ID which retrieves from LogInfo table

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

        child = storage.get(ChildProfile, child_id)
        if not child:
            return jsonify({'error': 'child not found'}), 404

        if not is_parent(child, user):
            return jsonify({'error': 'not authorised'}), 403

        appointments = child.appointments

        schedules = Schedule.query.filter(
            and_(
                Schedule.appointment_id.in_([a.id for a in appointments]),
                Schedule.status == 'complete'
            )
        ).all()

        # Group schedules by date
        appointments_by_date = defaultdict(list)
        for schedule in schedules:
            appointment = schedule.appointment

            if child.loginfo.account_type == 'child':
                name_ = appointment.practitioner.identity
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
