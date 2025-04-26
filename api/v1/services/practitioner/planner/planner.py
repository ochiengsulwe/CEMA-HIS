"""
The module retreives a practitioner's planner object
"""
from flask import jsonify

from flask_jwt_extended import get_jwt_identity

from sqlalchemy.exc import IntegrityError

from api.v1 import db

from models import storage
from models.loginfo import LogInfo
from models.planner import Planner


def planner():
    """
    Retrieves a planner for a practitioner.

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
        planner = Planner.query.filter_by(prac_profile_id=practitioner.id).first()
        if not planner:
            return jsonify({"error": "no planner yet."}), 404
        p_info = {
            "id": planner.id,
            "created_on": planner.created_at.strftime('%Y-%m-%d'),
            "created_at": planner.created_at.strftime('%H:%M'),
            "created_on_day": planner.created_at.strftime('%A')
        }
        return jsonify(p_info), 200
    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        db.session.rollback()
        return {"error": "An unexpected error occurred.", "details": str(e)}
