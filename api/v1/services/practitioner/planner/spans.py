"""
The module retreives a list of a day's available spans for a practitioner to be
    assigned an appointment
"""
from collections import defaultdict
from flask import jsonify

from flask_jwt_extended import get_jwt_identity

from sqlalchemy.exc import IntegrityError

from api.v1 import db

from models import storage
from models.loginfo import LogInfo
from models.slot import Slot


def days_spans(slot_id):
    """
    Retrieves all available day's spans recorded by creating a planner entry

    Returns:
        tuple: day's spans on success (or error message), with a matching HTTP code
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
        planner = practitioner.planner
        if not planner:
            return jsonify({'error': 'planner not found'}), 404

        slot = storage.get(Slot, slot_id)
        if not slot:
            return jsonify({"error": "slot not found."}), 404

        spans = slot.spans
        if not spans:
            return jsonify({"error": "spans not found."}), 404

        spans_by_day = defaultdict(list)
        for s in spans:
            s_info = {
                "id": s.id,
                "time_from": s.time_from.strftime('%H:%M'),
                "time_to": s.time_to.strftime('%H:%M')
            }
            spans_by_day[s.slot.date.strftime('%Y-%m-%d (%A)')].append(s_info)
        return jsonify(spans_by_day), 200
    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        db.session.rollback()
        return {"error": "An unexpected error occurred.", "details": str(e)}
