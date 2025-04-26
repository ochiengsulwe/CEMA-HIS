"""
Creates a prescription entry attached to a schedule
"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db

from models import storage
from models.loginfo import LogInfo
from models.prescription.patient_prescription import PatientPrescription
from models.schedule import Schedule

from utils.database import record_integrity


def create_prescription(schedule_id):
    """
    Creates a PatientPrescription object to hold all prescriptions of a schedule.

    Prescription is attached to Schedule but not Appointment for this very reasons:
        i. Every visit might require a unique Prescription for prescriptions might
            change with sysmptoms presented each time of a visit

    Args:
        schedule_id (str): the identifier of the current active/ongoing patient visit

    Returns:
        tuple: A response message containing Prescription ID or failure,
            with a HTTP code
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'error': 'not authorised'}), 403

    try:
        prac = storage.get(LogInfo, current_user_id)
        if not prac:
            return jsonify({'error': 'user account not found'}), 404

        profile = prac.prac_profile
        if not profile:
            return jsonify({'error': 'user account not found'}), 404
        schedule = storage.get(Schedule, schedule_id)
        if not schedule:
            return jsonify({'error': 'schedule not found'})
        if schedule.appointment not in profile.appointments:
            return jsonify({'error': 'not authorised'}), 403

        prescription = PatientPrescription.query.filter_by(
            schedule_id=schedule_id).first()

        if not prescription:
            pres = record_integrity(db.session, PatientPrescription,
                                    schedule_id=schedule_id)
            storage.save()
            return jsonify({'prescription_id': pres.id}), 200

        return jsonify({'prescription_id': prescription.id}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
