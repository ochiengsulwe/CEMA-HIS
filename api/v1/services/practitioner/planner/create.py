"""
The module creates a practitioner's Planner object
"""
from datetime import datetime
from flask import jsonify

from flask_jwt_extended import get_jwt_identity

from sqlalchemy.exc import IntegrityError

from api.v1 import db

from models import storage
from models.date import Date
from models.loginfo import LogInfo
from models.planner import Planner
from models.slot import Slot
from models.span import Span

from utils.create_planner import create_planner
from utils.database import record_integrity
from utils.general import data_check
from utils.overlap import check_schedule


def practitioner_create_planner(data):
    """
    Create a planner for a practitioner.

    A new Planner instance is created if doesn't exist, or creates a day's schedule
    (Slot instance) if the Planner instance exist.

    Args:
        data (dict): Dictionary containing time span information and date

    Returns:
        tuple: message (suceess or error), coupled with a matching HTTP response code.
    """
    try:
        required_fields = ['date', 'time_from', 'time_to']
        if not data:
            return jsonify({'message': 'not json'}), 400

        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'mesasge': 'not signed in'}), 401

        prac = storage.get(LogInfo, current_user_id)
        if not prac:
            return jsonify({'mesasge': 'practitioner logins not found'}), 404

        if prac.account_type != 'practitioner':
            return jsonify({'error': 'not authorised'}), 403

        practitioner = prac.prac_profile
        if practitioner is None:
            return jsonify({'mesasge': 'practitioner not found'}), 404

        date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        time_from = datetime.strptime(data['time_from'], '%H:%M').time()
        time_to = datetime.strptime(data['time_to'], '%H:%M').time()

        error_response = data_check(data, required_fields)
        if error_response:
            return error_response

        date_obj = Date.query.filter_by(date=date).first()
        if not date_obj:
            return jsonify({"error": "Invalid date."}), 400

        if time_to <= time_from:
            return jsonify({"error": "time_to must be greater than time_from."}), 400

        planner = Planner.query.filter_by(prac_profile_id=practitioner.id).first()
        if not planner:
            planner = record_integrity(db.session, Planner,
                                       practitioner=practitioner,
                                       )
            # storage.save()

            slot = record_integrity(db.session, Slot,
                                    planner=planner,
                                    date=date
                                    )
            # storage.save()

            span = record_integrity(db.session, Span,
                                    time_from=time_from,
                                    time_to=time_to,
                                    slot=slot
                                    )
            # storage.save()
            slot.spans.append(span)
            planner.slots.append(slot)
            planner.save()
            return jsonify({"message": "Planner created successfully."}), 201

        available_spans = check_schedule(
            db.session, practitioner, date, time_from, time_to
        )

        if isinstance(available_spans, tuple):
            return available_spans

        for span in available_spans:
            tf = datetime.strptime(span["time_from"], "%H:%M").time()
            tt = datetime.strptime(span["time_to"], "%H:%M").time()
            create_planner(db.session, practitioner.id, date, tf, tt)
        return jsonify({"message": "Planner created successfully."}), 201
    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        db.session.rollback()
        return {"error": "An unexpected error occurred.", "details": str(e)}
