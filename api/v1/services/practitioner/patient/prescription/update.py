from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from models import storage
from models.loginfo import LogInfo
from models.prescription.prescription_entry import PrescriptionEntry


def update_frequency(prescription_entry_id, update_data):
    """
    Updates the frequency of a given prescription entry.

    Args:
        prescription_entry_id (str): The ID of the PrescriptionEntry.
        update_data (dict): Dictionary of fields to update on the Frequency.

    Returns:
        tuple: JSON response with updated frequency info or error.
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

        freq = entry.frequency
        if not freq:
            return jsonify({'error': 'Frequency data not found for this entry'}), 404

        freq.update(update_data)

        if 'times' in update_data or 'start_time' in update_data:
            freq.at_ = freq.generate_times()
            freq.save()

        return jsonify({
            'message': 'Frequency updated successfully',
            'frequency': {
                'id': freq.id,
                'start_date': str(freq.start_date),
                'end_date': str(freq.end_date),
                'routine': freq.routine,
                'times': freq.times,
                'duration': freq.duration,
                'for_': freq.for_,
                'start_time': str(freq.start_time),
                'at_': freq.at_
            }
        }), 200

    except (SQLAlchemyError, KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 500
