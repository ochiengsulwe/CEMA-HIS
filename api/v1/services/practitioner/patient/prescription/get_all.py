"""
Retrieve all entries under a specific prescription, grouped by category and sub_category
"""

from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from collections import defaultdict

from models import storage
from models.loginfo import LogInfo
from models.prescription.patient_prescription import PatientPrescription


def get_prescription_entries(prescription_id):
    """
    Fetch all entries that belong to a specific prescription and group them
    by category and sub_category.

    Args:
        prescription_id (str): The unique ID of the prescription.

    Returns:
        tuple: A JSON response with grouped entries or an error message.
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
            return jsonify({'error': 'user profile not found'}), 404

        prescription = storage.get(PatientPrescription, prescription_id)
        if not prescription:
            return jsonify({'error': 'prescription not found'}), 404

        entries = prescription.entries

        grouped_entries = defaultdict(lambda: defaultdict(list))

        for entry in entries:
            entry_data = {
                'id': entry.id,
                'name': entry.name,
                'note': entry.note,
                'frequency': {
                    'id': entry.frequency.id,
                    'start_date': entry.frequency.start_date.isoformat(),
                    'start_time': entry.frequency.start_time.isoformat(),
                    'routine': entry.frequency.routine,
                    'times': entry.frequency.times,
                    'duration': entry.frequency.duration,
                    'for_': entry.frequency.for_
                } if entry.frequency else None
            }

            grouped_entries[entry.category][entry.sub_category or 'General'].append(
                entry_data)

        response = {
            category: {
                sub_cat: items for sub_cat, items in sub_dict.items()
            }
            for category, sub_dict in grouped_entries.items()
        }

        return jsonify({'entries': response}), 200

    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
