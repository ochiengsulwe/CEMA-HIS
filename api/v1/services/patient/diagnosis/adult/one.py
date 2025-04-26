"""
Service to retrieve a specific diagnosis for the authenticated adult.
"""

from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.diagnosis import Diagnosis


def get_specific_diagnosis(diagnosis_id):
    """
    Retrieves a specific diagnosis for the authenticated adult user by diagnosis ID.

    Args:
        diagnosis_id (str): The unique ID of the diagnosis to retrieve.

    Returns:
        tuple: JSON response with diagnosis details or error message,
            and HTTP status code.
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        if user.account_type != 'adult':
            return jsonify({'error': 'not authorised'}), 403

        diagnosis = storage.get(Diagnosis, diagnosis_id)
        if not diagnosis:
            return jsonify({'error': 'diagnosis not found'}), 404

        appointment_ids = [a.id for a in user.adult_profile.appointments]
        if diagnosis.appointment_id not in appointment_ids:
            return jsonify({'error': 'not authorised to access this diagnosis'}), 403

        practitioner = diagnosis.schedule.appointment.practitioner.identity
        practitioner_name = " ".join(filter(None, [
            practitioner.first_name,
            practitioner.middle_name,
            practitioner.last_name
        ]))

        diagnosis_details = {
            "diagnosis": diagnosis.diagnosis,
            "severity": diagnosis.severity,
            "prognosis": diagnosis.prognosis,
            "diagnosed_by": practitioner_name,
            "schedule_id": diagnosis.schedule_id,
            "appointment_id": diagnosis.appointment_id,
            "created_at": diagnosis.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        return jsonify(diagnosis_details), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
