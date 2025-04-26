"""
The module deletes practitioner's selected free time.
"""
from flask import jsonify

from flask_jwt_extended import get_jwt_identity

from sqlalchemy.exc import IntegrityError

from api.v1 import db

from models import storage
from models.span import Span


def practitioner_delete_span(span_id):
    """
    Removes a specific time entry from practitioner's availability

    Args:
        span_id (str): the specific time's unique ID

    Returns:
        tuple: message (suceess or error), coupled with a matching HTTP response code.
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        span = storage.get(Span, span_id)
        if not span:
            return jsonify({'error': 'span not found!'}), 404

        if span.slot.planner.practitioner.loginfo_id != current_user_id:
            return jsonify({'error': 'forbidden'}), 403

        span.delete()
        storage.save()

        return jsonify({'message': 'span successfully deleted'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        db.session.rollback()
        return {"error": "An unexpected error occurred.", "details": str(e)}
