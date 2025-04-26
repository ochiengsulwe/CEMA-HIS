"""
This module defines how all complete patient appointments relating to the
    practitioner will be retrieved
"""
from sqlalchemy import and_
from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.schedule import Schedule


def complete_appointments(loginfo_id):
    """
        Retrieves all related patient complete appointments for the authenticated
            practitioner.

        Args:
            loginfo_id (str): patient's unique identifier

        Returns:
            tuple: response containing a list of complete appointments or an error
                message.
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'mesasge': 'user not found'}), 404

        patient = storage.get(LogInfo, loginfo_id)
        if not patient:
            return jsonify({'error': 'patient not found'}), 404

        if patient.account_type == 'adult':
            profile = patient.adult_profile
            identity = profile.identity
        elif patient.account_type == 'child':
            profile = patient.child_profile
            identity = profile.identity

        if user.account_type != 'practitioner':
            return jsonify({'error': 'not authorised'}), 403

        prac = user.prac_profile
        if not prac:
            return jsonify({'error': 'practitioner account does not exist'}), 404

        appts = [app for app in profile.appointments if app.practitioner == prac]
        if not appts:
            return jsonify({'error': 'no appointments with the patient'}), 404

        schedules = Schedule.query.filter(
            and_(
                Schedule.appointment_id.in_([a.id for a in appts]),
                Schedule.status == 'pending'
            )
        ).all()
        """
        if not schedules:
            return jsonify({'error': 'schedules not found'}), 404
        """
        first_name = identity.first_name
        middle_name = identity.middle_name
        last_name = identity.last_name
        name = " ".join(filter(None, [first_name, middle_name, last_name]))

        appointments_by_date = defaultdict(list)
        for schedule in schedules:
            appointment_details = {
                "start_time": schedule.time_from.strftime("%H:%M"),
                "end_time": schedule.time_to.strftime("%H:%M"),
                "appointment_status": schedule.appointment.status,
                "appointment_type": schedule.appointment.type,
                "appointment_state": schedule.status,
                "appointment_with": name,
                "appointment_schedule_id": schedule.id,
                "day_of_week": schedule.date.strftime('%A')
            }
            appointments_by_date[schedule.date.strftime('%Y-%m-%d')].append(
                appointment_details)

        return jsonify(appointments_by_date), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
