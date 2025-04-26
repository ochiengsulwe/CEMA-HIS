"""
The module creates a practitioner's free time in a day.
"""
from datetime import datetime, timedelta
from flask import jsonify
from sqlalchemy.exc import IntegrityError

from models import storage
from models.date import Date
from models.planner import Planner
from models.practitioner_profile import PracProfile
from models.slot import Slot
from models.span import Span

from utils.database import record_integrity


def create_planner(session, prac_id, date, time_from, time_to):
    """
    Adds date and associated availability times to practitioner's planner object


    This method not necessarily creates a planner object as the name suggest (I admit
        the name is misleading), but components of the planner object itself
    The components of a planner (which this method is responsible for creating) are:
        i. The Associated Date/Day - the specific day the practitioner will be available
        ii. Time spans - the associaed time availability ranges

    Args:
        session (Session): The current sqlalchemy session
        prac_id (str): The ID of the current practitioner in appointment
        date (datetime.date): The appointment date
        time_from (datetime.time): The appointment start time
        time_to (datetime.time): The appointment end time
    """
    try:
        practitioner = storage.get(PracProfile, prac_id)
        if not practitioner:
            return jsonify({'error': 'practitioner not found'}), 404

        date_obj = Date.query.filter_by(date=date).first()
        if not date_obj:
            return jsonify({"error": "invalid date"}), 404

        if time_to <= time_from:
            return jsonify({"error": "time_to must be greater than time_from"}), 400

        planner = Planner.query.filter_by(prac_profile_id=practitioner.id).first()
        if not planner:
            return jsonify({'error': 'practitioner planner not found'}), 404
        # Check for duplicate or overlapping time slots for an existing Date
        this_slot = Slot.query.filter(
                Slot.planner_id == planner.id,
                Slot.date == date
                ).first()

        if this_slot:
            merged_time_from = time_from
            merged_time_to = time_to

            # Iterate through existing spans to check for adjacency or overlap
            spans_to_remove = []
            for span in this_slot.spans:
                existing_time_from = span.time_from
                existing_time_to = span.time_to
                to_ = datetime.combine(datetime.today(), time_to)
                fro_ = datetime.combine(datetime.today(), time_from)
                time_fro = (fro_ - timedelta(minutes=5)).time()
                time_t = (to_ + timedelta(minutes=5)).time()
                # Check for overlap
                if (
                        (time_fro <= existing_time_to and
                         time_t >= existing_time_from
                         )
                ) or (
                        (time_fro >= existing_time_to and
                         time_t <= existing_time_from
                         )
                     ):
                    # Update merged slot bounds
                    merged_time_from = min(merged_time_from, existing_time_from)
                    merged_time_to = max(merged_time_to, existing_time_to)
                    # Mark this slot for removal
                    spans_to_remove.append(span)
            # Remove the slots that were merged
            for span in spans_to_remove:
                span.delete()

            span = record_integrity(session, Span,
                                    time_from=merged_time_from,
                                    time_to=merged_time_to,
                                    slot=this_slot
                                    )
            session.add(span)
            session.commit()

            return
        slot = record_integrity(session, Slot,
                                planner=planner,
                                date=date
                                )
        span = record_integrity(session, Span,
                                time_from=time_from,
                                time_to=time_to,
                                slot=slot
                                )
        slot.spans.append(span)
        session.add(slot)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        session.rollback()
        return {"error": "An unexpected error occurred.", "details": str(e)}
