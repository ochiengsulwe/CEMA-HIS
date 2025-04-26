"""
This module defines how a specific diagnosis for a child is retrieved.

Only authenticated parents who are linked to the child can retrieve the diagnosis.
"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.child_profile import ChildProfile
from models.loginfo import LogInfo
from models.diagnosis import Diagnosis
from utils.support import is_parent


def retrieve_child_diagnosis(child_id, diagnosis_id):
    """
    Retrieves a specific diagnosis for a child via an authenticated parent's account.

    Args:
        child_id (str): The ID of the child (from ChildProfile table)
        diagnosis_id (str): The ID of the diagnosis to retrieve

    Returns:
        tuple: response containing diagnosis details or an error message,
            and HTTP response code
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

        diagnosis = storage.get(Diagnosis, diagnosis_id)
        if not diagnosis:
            return jsonify({'error': 'diagnosis not found'}), 404

        child_schedule_ids = [
            schedule.id for appointment in child.appointments for schedule in
            appointment.schedules
        ]

        if diagnosis.schedule_id not in child_schedule_ids:
            return jsonify({'error': 'not authorised to access this diagnosis'}), 403

        diagnosis_details = {
            "id": diagnosis.id,
            "diagnosis": diagnosis.diagnosis,
            "severity": diagnosis.severity,
            "prognosis": diagnosis.prognosis,
            "schedule_id": diagnosis.schedule_id,
            "appointment_id": diagnosis.schedule.appointment_id,
            "diagnosed_by": " ".join(filter(None, [
                diagnosis.schedule.appointment.practitioner.identity.first_name,
                diagnosis.schedule.appointment.practitioner.identity.middle_name,
                diagnosis.schedule.appointment.practitioner.identity.last_name
            ])),
            "created_at": diagnosis.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

        return jsonify(diagnosis_details), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
