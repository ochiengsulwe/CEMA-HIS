from datetime import timedelta

from flask import jsonify

from api.v1 import db
from models.date import Date
from models.planner import Planner
from models.span import Slot


def portion_slots(slot):
    """
    Adjusts practitioner's time slot to fit in chunks of 20 minutes

    Args:
        slot(obj): The slot to be adjusted

    Returns:
        List(dict): A list of time time object dictionaries.
    """
    time_slots = []
    current_time = slot.time_from

    while current_time < slot.time_to:
        end_time = current_time + timedelta(minutes=15)
        if end_time > slot.time_to:
            break

        time_slots.append({
            'time_from': current_time,
            'time_to': end_time
        })

        # Add 5 minutes of space between slots
        current_time = end_time + timedelta(minutes=5)

    return time_slots


def chunk(practitioner_id, date):
    """
    Portions practitioner's free slots into 15 minutes each, with a 5 minutes space.

    Args:
        practitioner_id (str): The practitioner's ID.
        date (datetime.date): The date of the appointment.

    Returns:
        List[obj: datetime.time]: A list of chunked time
    """
    try:
        # Fetch the practitioner's planner for the given date
        planner = db.session.query(Planner).join(Date).filter(
            Planner.prac_profile_id == practitioner_id,
            Date.date == date
        ).first()
        if not planner:
            return jsonify({'error': 'Planner not found for the practitioner'}), 404

        slots = db.session.query(Slot).filter_by(
            planner_id=planner.id).all()

        if not slots:
            return jsonify({'error': 'No free time found for the given date'}), 404

        all_time_chunks = []
        for slot in slots:
            time_diff = (slot.time_to - slot.time_from).total_seconds() / 60

            if time_diff % 20 != 0:
                # Extend slot time_to to the nearest multiple of 20
                extra_minutes = 20 - (time_diff % 20)
                slot.time_to += timedelta(minutes=extra_minutes)
                db.session.add(slot)

            # Portion the slot into 15-minute chunks with 5-minute gaps
            time_chunks = portion_slots(slot)
            all_time_chunks.extend(time_chunks)

        db.session.commit()

        return jsonify({'time_chunks': all_time_chunks}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
