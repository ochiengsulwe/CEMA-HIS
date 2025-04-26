from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from models import storage
from models.loginfo import LogInfo
from models.prescription.prescription_entry import PrescriptionEntry


def delete_prescription_entry(prescription_entry_id):
    """
    Delete a PrescriptionEntry by its ID.

    Args:
        prescription_entry_id (str): The ID of the PrescriptionEntry to delete.

    Returns:
        tuple: JSON response with a message or error.
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'error': 'Not authorized'}), 403

    try:
        prac = storage.get(LogInfo, current_user_id)
        if not prac or not prac.prac_profile:
            return jsonify({'error': 'User not found'}), 404

        entry = storage.get(PrescriptionEntry, prescription_entry_id)
        if not entry:
            return jsonify({'error': 'Prescription entry not found'}), 404

        storage.delete(entry)
        storage.save()

        return jsonify(
            {
                'message': 'Prescription entry deleted successfully'}
        ), 200

    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
