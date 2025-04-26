from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo


def get_prescription(prescription_id):
    """
    Retrieves a specific prescription for an authenticated adult patient.

    Args:
        prescription_id (str): ID of the PatientPrescription record

    Returns:
        tuple: response containing the prescription information or an error message,
               and the associated HTTP response code
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'error': 'user not authorized'}), 403

        adult = user.adult_profile
        if not adult:
            return jsonify({'error': 'not authorized'}), 403

        for appointment in adult.appointments:
            for schedule in appointment.schedules:
                prescription = schedule.prescription
                if prescription and prescription.id == prescription_id:
                    prescription_data = []
                    for entry in prescription.pre_entries:
                        frequency_data = None
                        if entry.frequency:
                            frequency_data = {
                                "start_date":
                                (entry.frequency.start_date.strftime('%Y-%m-%d') if
                                 entry.frequency.start_date else None),
                                "end_date":
                                (entry.frequency.end_date.strftime('%Y-%m-%d') if
                                 entry.frequency.end_date else None),
                                "routine": entry.frequency.routine,
                                "times": entry.frequency.times,
                                "duration": entry.frequency.duration,
                                "for": entry.frequency.for_,
                                "start_time":
                                (entry.frequency.start_time.strftime('%H:%M') if
                                 entry.frequency.start_time else None),
                                "at": entry.frequency.at_
                            }

                        prescription_data.append({
                            "prescription_id": prescription.id,
                            "status": prescription.status,
                            "category": entry.category,
                            "sub_category": entry.sub_category,
                            "name": entry.name,
                            "note": entry.note,
                            "frequency": frequency_data,
                            "prescribed_by": (
                                schedule.appointment.practitioner.identity.full_name
                                if schedule.appointment.practitioner
                                else None
                            ),
                            "prescription_date": (
                                prescription.created_at.strftime('%Y-%m-%d'))
                        })

                    return jsonify(prescription_data), 200

        return jsonify({'error': 'prescription not found'}), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'database error', 'details': str(e)}), 500
