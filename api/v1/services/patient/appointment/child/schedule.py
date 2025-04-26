"""
This module defines how a single is appointment schedule is retrieved for child only.
"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.child_profile import ChildProfile
from models.schedule import Schedule
from models.loginfo import LogInfo
from utils.support import is_parent


def this_child_schedule(schedule_id, child_id):
    """
        Retrieves a single appointment schedule for authenticated user's child

        Args:
            appointment_id (str): The ID of the appointment to retrieve.
            child_id (str): child's ID

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

        child = storage.get(ChildProfile, child_id)
        if not child:
            return jsonify({'error': 'user not found'}), 404

        if not is_parent(child, user):
            return jsonify({'error': 'not authorised'}), 403

        schedule = storage.get(Schedule, schedule_id)
        if not schedule:
            return jsonify({'error': 'appointment schedule not found'}), 404

        if schedule.appointment not in child.appointments:
            return jsonify({'error': 'not authorised'}), 403

        schedule_dets = {
            "date": schedule.date.strftime('%Y-%m-%d'),
            "start_time": schedule.time_from.strftime("%H:%M"),
            "end_time": schedule.time_to.strftime("%H:%M"),
            "status": schedule.status,
            "id": schedule.id
            }

        return jsonify(schedule_dets), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
