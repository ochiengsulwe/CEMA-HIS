"""
The module deletes practitioner's entire day free time.
"""
from flask import jsonify

from flask_jwt_extended import get_jwt_identity

from sqlalchemy.exc import IntegrityError

from api.v1 import db

from models import storage
from models.slot import Slot


def practitioner_clear_day(slot_id):
    """
    Clears practitioner's day, by deleting all sloted times of the day

    Args:
        slot_id (str): the day's unique ID to be cleared

    Returns:
        tuple: message (suceess or error), coupled with a matching HTTP response code.
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        slot = storage.get(Slot, slot_id)
        if not slot:
            return jsonify({'error': 'slot not found'}), 404

        if slot.planner.practitioner.loginfo_id != current_user_id:
            return jsonify({'error': 'forbidden'}), 403

        slot.delete()
        storage.save()

        return jsonify({'message': 'your day is successfully cleared'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        db.session.rollback()
        return {"error": "An unexpected error occurred.", "details": str(e)}
