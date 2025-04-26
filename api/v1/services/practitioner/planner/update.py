"""
The module updates practitioner's entered free times.
"""
from datetime import datetime
from flask import jsonify

from flask_jwt_extended import get_jwt_identity

from sqlalchemy.exc import IntegrityError

from api.v1 import db

from models import storage
from models.span import Span

from utils.database import record_integrity
from utils.general import data_check


def practitioner_update_planner_time(data, span_id):
    """
    Updates a planner for a practitioner.

    Args:
        data (dict): Dictionary containing new_start_time' and 'new_end_time'

    Returns:
        tuple: message (suceess or error), coupled with a matching HTTP response code.
    """
    try:
        required_fields = ['new_time_from', 'new_time_to']
        if not data:
            return jsonify({'message': 'not json'}), 400

        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        error_response = data_check(data, required_fields)
        if error_response:
            return error_response

        new_time_from = datetime.strptime(data['new_time_from'], '%H:%M').time()
        new_time_to = datetime.strptime(data['new_time_to'], '%H:%M').time()

        span = storage.get(Span, span_id)
        if not span:
            return jsonify({'error': 'span not found'}), 404

        slot = span.slot
        if not slot:
            return jsonify({'error': 'slot not found'}), 404

        if slot.planner.practitioner.loginfo_id != current_user_id:
            return jsonify({'error': 'Not authorised'}), 403

        if new_time_to <= new_time_from:
            return jsonify({"error": "time_to must be greater than time_from."}), 400

        spans = slot.spans
        if spans:
            overlapping_spans = [sp for sp in spans if sp.slot_id == slot.id and
                                 sp.time_from <= new_time_to and
                                 sp.time_to >= new_time_from]

            if overlapping_spans and len(overlapping_spans) > 1:
                min_time_from = min([s.time_from for s in overlapping_spans] +
                                    [new_time_from])
                max_time_to = max([s.time_to for s in overlapping_spans] +
                                  [new_time_to])

                for s in overlapping_spans:
                    s.delete()
                storage.save()

                merged_span = record_integrity(db.session, Span,
                                               time_from=min_time_from,
                                               time_to=max_time_to,
                                               slot=slot
                                               )
                merged_span.save()

                return jsonify({"message": "time updated successfully."}), 201

            elif (
                span and
                new_time_from == span.time_from and
                new_time_to == span.time_to
            ):
                mes = 'You have entered same time as previous'
                return jsonify({'error': mes}), 409

            elif span:
                span.time_from = new_time_from
                span.time_to = new_time_to
                span.save()
                return jsonify({"message": "time updated successfully."}), 201
            else:
                return jsonify({'error': 'invalid span'}), 400
        else:
            return jsonify({'error': 'slot has no spans yet'}), 404
    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        db.session.rollback()
        return {"error": "An unexpected error occurred.", "details": str(e)}
