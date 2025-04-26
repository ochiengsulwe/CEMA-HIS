"""
This module defines how a specific appointment schedule is retrieved
"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.schedule import Schedule
from models.loginfo import LogInfo


def this_schedule(schedule_id):
    """
        Retrieves a specific appointment schedule for the associated authenticated user

        This helps in retrieving schedules for manupulation and view

        Args:
            schedule_id (str): The ID of the appointment schedule to retrieve.

        Returns:
           tuple: response containing an appointment schedule object and an HTTP code.
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        schedule = storage.get(Schedule, schedule_id)
        if not schedule:
            return jsonify({'error': 'schedule not found'}), 404

        schedule_info = {
            "date": schedule.date.strftime('%Y-%m-%d'),
            "start_time": schedule.time_from.strftime("%H:%M"),
            "end_time": schedule.time_to.strftime("%H:%M"),
            "status": schedule.status,
            "id": schedule.id
            }
        return jsonify(schedule_info), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
