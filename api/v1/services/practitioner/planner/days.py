"""
The module retreives a list of days available for a practitioner to be assigned an
    appointment
"""
from collections import defaultdict
from flask import jsonify

from flask_jwt_extended import get_jwt_identity

from sqlalchemy.exc import IntegrityError

from api.v1 import db

from models import storage
from models.loginfo import LogInfo
from models.slot import Slot

from utils.support import week_of_month


def get_available_days():
    """
    Retrieves all available days as recorded by creating a planner entry

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
        planner = practitioner.planner
        if not planner:
            return jsonify({'error': 'planner not found'}), 404

        slots = Slot.query.filter_by(planner=planner).all()
        if not slots:
            return jsonify({"error": "all days are booked."}), 404
        days_by_order = defaultdict(list)
        for s in slots:
            s_info = {
                "id": s.id,
                "day": s.date.strftime('%A'),
                "day_of_year": s.date.strftime('%j'),
                "week_of_year": s.date.strftime('%U'),  # Sunday as first day
                "week_of_month": str(week_of_month(s.date))
            }
            days_by_order[s.date.strftime('%Y-%m-%d')].append(s_info)
        return jsonify(days_by_order), 200
    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        db.session.rollback()
        return {"error": "An unexpected error occurred.", "details": str(e)}
