"""
Allow a practitioner to input various prescription to a patient
"""

from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db

from models import storage
from models.loginfo import LogInfo
from models.prescription.frequency import Frequency
from models.prescription.patient_prescription import PatientPrescription
from models.prescription.prescription_entry import PrescriptionEntry

from utils.database import record_integrity


def enter_prescription(data, prescription_id):
    """
    Enables prescription entry by a practitioner.

    This allows for a list or just a single prescription entry at a time

    Args:
        data (dict): a dictionary containing attributes to used in the symptom creation
        prescription_id (str): the prescription holder

    Returns:
        tuple: A response message indicating success or failure, with an HTTP code
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'error': 'not authorised'}), 403

    if not data:
        return jsonify({'error': 'not json'}), 400

    try:
        prac = storage.get(LogInfo, current_user_id)
        if not prac:
            return jsonify({'error': 'user account not found'}), 404
        profile = prac.prac_profile
        if not profile:
            return jsonify({'error': 'user account not found'}), 404
        prescription = storage.get(PatientPrescription, prescription_id)
        if not prescription:
            return jsonify({'error': 'prescription entry not found'}), 404

        for entry_data in data['entries']:
            required_fields = ['category', 'name']
            if not all(field in entry_data for field in required_fields):
                return jsonify(
                    {'error': f'Missing fields in entry: {required_fields}'}
                ), 400

            frequency = None
            freq_data = entry_data.get('frequency')
            if freq_data:
                frequency = record_integrity(db.session, Frequency,
                                             start_date=freq_data['start_date'],
                                             start_time=freq_data['start_time'],
                                             routine=freq_data['routine'],
                                             times=freq_data.get('times'),
                                             duration=freq_data.get('duration'),
                                             for_=freq_data.get('for_')
                                             )
                storage.save()

            prescription_entry = record_integrity(db.session, PrescriptionEntry,
                                                  category=entry_data['category'],
                                                  sub_category=entry_data.get(
                                                      'sub_category'),
                                                  name=entry_data['name'],
                                                  note=entry_data.get('note'),
                                                  frequency=frequency,
                                                  prescription=prescription
                                                  )

            prescription_entry.save()

        return jsonify({'message': 'prescription(s) entered successfully'}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
