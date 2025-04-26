"""
This module defines how a patient's info is  retrieved for an authenticated prac
"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo


def this_patient(loginfo_id):
    """
        Retrieves a patient info for the authenticated practitioner.

        Args:
            loginfo_id (str): patients's unique identifier
        Returns:
            tuple: JSON response containing a dictionary details,
               or an error message with appropriate status code.
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        if user.account_type == 'practitioner':
            appointments = user.prac_profile.appointments
            if not appointments:
                return jsonify({'error': 'no appointment yet'}), 404

            patient = storage.get(LogInfo, loginfo_id)
            if not patient:
                return jsonify({'error': 'patient data not found'}), 404

            if patient.adult_profile is not None:
                identity = patient.adult_profile.identity
            elif patient.child_profile is not None:
                identity = patient.child_profile.identity
            else:
                return jsonify({'error': 'not authorised'}), 403

            first_name = identity.first_name
            middle_name = identity.middle_name
            last_name = identity.last_name
            name = " ".join(filter(None, [first_name, middle_name, last_name]))

            patient_details = {
                "name": name,
                "age": str(identity.age),
                "gender": identity.gender,
                "loginfo_id": patient.id,
                "patient_type": patient.account_type
            }
            return jsonify(patient_details), 200
        else:
            return jsonify({'error': 'not authorised'}), 403
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
