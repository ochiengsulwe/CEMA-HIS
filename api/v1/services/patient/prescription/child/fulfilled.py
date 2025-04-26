from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from models import storage
from models.child_profile import ChildProfile
from models.loginfo import LogInfo
from utils.support import is_parent


def fulfilled_prescriptions(child_id):
    """
    Retrieves all 'fulfilled' prescriptions for an adult patient's child, grouped by
        prescription date.

    Args:
        child_id (str): user's child

    Returns:
        tuple: response containing grouped prescriptions or an error message, and
               associated HTTP response code
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        adult = user.adult_profile
        if not adult:
            return jsonify({'error': 'not authorised'}), 403

        child = storage.get(ChildProfile, child_id)
        if not child:
            return jsonify({'error': 'child not found'}), 404

        if not is_parent(child, user):
            return jsonify({'error': 'not authorised'}), 403

        grouped_prescriptions = defaultdict(list)

        for appointment in child.appointments:
            for schedule in appointment.schedules:
                prescription = schedule.prescription
                if prescription and prescription.status == 'fulfilled':
                    practitioner = (
                        schedule.appointment.practitioner.idenity
                        if schedule.appointment and
                        schedule.appointment.practitioner.identity
                        else None
                    )
                    practitioner_name = (
                        f"{practitioner.first_name} "
                        f"{practitioner.middle_name or ''} "
                        f"{practitioner.last_name}"
                        if practitioner else None
                    ).strip()

                    prescription_date = prescription.created_at.date().isoformat()

                    for entry in prescription.pre_entries:
                        frequency_details = None
                        if entry.frequency:
                            frequency_details = {
                                "start_date": (entry.frequency.start_date.strftime(
                                    '%Y-%m-%d')
                                 if entry.frequency.start_date else None),
                                "end_date": (entry.frequency.end_date.strftime(
                                    '%Y-%m-%d') if entry.frequency.end_date else None),
                                "routine": entry.frequency.routine,
                                "times": entry.frequency.times,
                                "duration": entry.frequency.duration,
                                "for_": entry.frequency.for_,
                                "start_time": (entry.frequency.start_time.strftime(
                                    '%H:%M:%S')
                                 if entry.frequency.start_time else None),
                                "at": entry.frequency.at_,
                            }

                        grouped_prescriptions[prescription_date].append({
                            "prescription_id": prescription.id,
                            "status": prescription.status,
                            "category": entry.category,
                            "sub_category": entry.sub_category,
                            "name": entry.name,
                            "note": entry.note,
                            "frequency": frequency_details,
                            "prescribed_by": practitioner_name,
                            "prescription_date": prescription_date
                        })

        return jsonify(grouped_prescriptions), 200

    except SQLAlchemyError as e:
        return jsonify({'error': 'database error', 'details': str(e)}), 500

    except Exception as e:
        return jsonify({'error': 'unexpected error', 'details': str(e)}), 500
