"""
This module defines how all prescriptions will be retrieved for adults only.

No filtering in this case, all prescriptions tied to schedules are retrieved.
A very expensive transaction.
"""
from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.schedule import Schedule


def all_prescriptions():
    """
    Retrieves all prescriptions for the authenticated adult user.

    Returns:
        tuple: response containing a list of prescriptions or an error message, and
        associated HTTP response code
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        if user.account_type != 'adult':
            return jsonify({'error': 'not authorised'}), 403

        appointments = user.adult_profile.appointments

        schedules = Schedule.query.filter(
            Schedule.appointment_id.in_([a.id for a in appointments])
        ).all()

        prescriptions_by_date = defaultdict(list)
        for schedule in schedules:
            if schedule.prescription:
                prescription = schedule.prescription

                practitioner = schedule.appointment.practitioner.identity
                practitioner_name = (
                    f"{practitioner.first_name} "
                    f"{practitioner.middle_name or ''} "
                    f"{practitioner.last_name}"
                ).strip()

                prescription_details = {
                    "prescription_id": prescription.id,
                    "schedule_id": schedule.id,
                    "appointment_id": schedule.appointment.id,
                    "status": prescription.status,
                    "created_at": prescription.created_at.strftime('%Y-%m-%d %H:%M'),
                    "prescribed_by": practitioner_name,
                    "entries": []
                }

                for entry in prescription.pre_entries:
                    frequency_details = None
                    if entry.frequency:
                        frequency_details = {
                            "start_date":
                            (entry.frequency.start_date.strftime('%Y-%m-%d') if
                             entry.frequency.start_date else None),
                            "end_date": (entry.frequency.end_date.strftime(
                                '%Y-%m-%d') if entry.frequency.end_date else None),
                            "routine": entry.frequency.routine,
                            "times": entry.frequency.times,
                            "duration": entry.frequency.duration,
                            "for_": entry.frequency.for_,
                            "start_time":
                            (entry.frequency.start_time.strftime('%H:%M:%S') if
                             entry.frequency.start_time else None),
                            "at": entry.frequency.at_,
                        }

                    entry_details = {
                        "category": entry.category,
                        "sub_category": entry.sub_category,
                        "name": entry.name,
                        "note": entry.note,
                        "frequency": frequency_details
                    }
                    prescription_details["entries"].append(entry_details)

                prescriptions_by_date[schedule.date.strftime('%Y-%m-%d')].append(
                    prescription_details)

        return jsonify(prescriptions_by_date), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'database error', 'details': str(e)}), 500

    except Exception as e:
        return jsonify({'error': 'unexpected error', 'details': str(e)}), 500
