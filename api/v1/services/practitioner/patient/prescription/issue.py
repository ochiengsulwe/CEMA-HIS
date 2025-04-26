"""
This confirms that a prescription entry is confirmed
"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db

from models import storage
from models.loginfo import LogInfo
from models.prescription.patient_prescription import PatientPrescription


def issue_prescription(prescription_id):
    """
    Affirms that a prescription object is complete and ready to be received by a
        pharmacy.

    What this technically does is to update the `prescription.status` from the default
        `draft` to `issued`.

    Args:
        prescription_id (str): the prescription entry to be updated.

    Returns:
        tuple: A response message containing Prescription ID or failure,
            with a HTTP code
    """

    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'error': 'not authorised'}), 403

    try:
        prac = storage.get(LogInfo, current_user_id)
        if not prac:
            return jsonify({'error': 'user account not found'}), 404

        profile = prac.prac_profile
        if not profile:
            return jsonify({'error': 'user account not found'}), 404

        prescription = storage.get(PatientPrescription, prescription_id)
        if not prescription:
            return jsonify({'error': 'prescription not found'}), 404

        if prescription.update({'status': 'issued'}):
            return jsonify({'message': 'prescription issued successfuly'}), 200

        return ({'error': 'unexpected error'}), 500

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
