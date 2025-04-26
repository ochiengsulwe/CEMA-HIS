"""
Retrieve a single prescription entry with full frequency details
"""

from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from models import storage
from models.loginfo import LogInfo
from models.prescription.prescription_entry import PrescriptionEntry


def get_prescription_entry_details(prescription_entry_id):
    """
    Fetch a single PrescriptionEntry by ID, including frequency details.

    Args:
        prescription_entry_id (str): The unique ID of the prescription entry.

    Returns:
        tuple: JSON response with entry details or an error message.
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

        fre = entry.frequency

        response = {
            'id': entry.id,
            'name': entry.name,
            'note': entry.note,
            'category': entry.category,
            'sub_category': entry.sub_category,
            'frequency': {
                'start_date': fre.start_date.isoformat() if fre else None,
                'start_time': fre.start_time.isoformat() if fre else None,
                'routine': fre.routine if fre else None,
                'times': fre.times if fre else None,
                'duration': fre.duration if fre else None,
                'for_': fre.for_ if fre else None,
                'end_date': fre.end_date.isoformat() if fre and fre.end_date else None,
                'at_': fre.at_ if fre and fre.at_ else []
            } if fre else None
        }

        return jsonify({'entry': response}), 200

    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
