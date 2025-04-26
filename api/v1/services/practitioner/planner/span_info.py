"""
The module retreives a practitioner's planner object
"""
from flask import jsonify

from flask_jwt_extended import get_jwt_identity

from sqlalchemy.exc import IntegrityError

from api.v1 import db

from models import storage
from models.loginfo import LogInfo
from models.slot import Slot
from models.span import Span


def span_info(slot_id, span_id):
    """
    Retrieves a planner  span information for a practitioner.

    Args:
    slot_id (str): day's unique entry
        span_id (str): time entry unique ID
    Returns:
        tuple: planner on success (or error message), coupled with a matching HTTP code
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        prac = storage.get(LogInfo, current_user_id)
        if not prac:
            return jsonify({'error': 'practitioner logins not found'}), 404
        practitioner = prac.prac_profile
        if practitioner is None:
            return jsonify({'error': 'practitioner not found'}), 404

        slot = storage.get(Slot, slot_id)
        if not slot:
            return jsonify({'error': 'slot not found'}), 404

        span = storage.get(Span, span_id)
        if not span:
            return jsonify({"error": "span not found."}), 404

        if span not in slot.spans:
            return jsonify({'error': 'not authorised'}), 403
        if span.slot not in practitioner.planner.slots:
            return jsonify({"error": "not authorised"}), 403

        s_info = {
            "id": span.id,
            "time_from": span.time_from.strftime('%H:%M'),
            "time_to": span.time_to.strftime('%H:%M'),
            "date": span.slot.date.strftime('%Y-%m-%d'),
            "day": span.slot.date.strftime('%A')
        }
        return jsonify(s_info), 200
    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        db.session.rollback()
        return {"error": "An unexpected error occurred.", "details": str(e)}
