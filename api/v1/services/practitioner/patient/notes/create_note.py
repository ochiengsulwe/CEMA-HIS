"""
The module creates a practitioner's note
"""
from flask import jsonify

from flask_jwt_extended import get_jwt_identity

from sqlalchemy.exc import IntegrityError

from api.v1 import db

from models import storage
from models.doctors_note import DoctorNote
from models.loginfo import LogInfo
from models.schedule import Schedule

from utils.database import record_integrity
from utils.general import data_check


def create_notes(data, schedule_id):
    """
    Create a note entry for a practitioner in consultation

    A doctor's Note always contain:
        i. note: a combination of both subjective and objective symptom analysis
        ii. assessment: a general view of what the patient might be suffering from.
            This often migh be used to deduce diagnosis or preceed diagnostic tests

    Args:
        data (dict): Dictionary containing notes and assessment information
        schedule_id (str): current appointment session identifier.

    Returns:
        tuple: message (suceess or error), coupled with a matching HTTP response code.
    """
    try:
        required_fields = ['note', 'assessment']
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

        schedule = storage.get(Schedule, schedule_id)
        if not schedule:
            return jsonify({'error': 'schedule entry not found'}), 404

        appt = schedule.appointment
        if not appt:
            return jsonify({'error': 'appointment info not found'}), 404
        if appt not in practitioner.appointments:
            return jsonify({'error': 'not authorised'}), 403

        note = data.get('note')
        assessment = data.get('assessment')

        error_response = data_check(data, required_fields)
        if error_response:
            return error_response

        note = record_integrity(db.session, DoctorNote,
                                note=note,
                                assessment=assessment,
                                schedule=schedule
                                )
        storage.save()

        return jsonify({'message': 'notes successfuly created'}), 201

    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        db.session.rollback()
        return {"error": "An unexpected error occurred.", "details": str(e)}
