"""
The module appends to an existing practitioner's note
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


def update_note(data, schedule_id):
    """
    Appends to an existing a note entry for a practitioner in consultation

    Args:
        data (dict): Dictionary containing new notes to be appended and
         new assessment information to be included
        schedule_id (str): unique appointment-in-place identifier

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

        existing_note = DoctorNote.query.filter_by(
            schedule_id=schedule.id).order_by(DoctorNote.created_at.desc()).first()
        if existing_note:
            existing_note.note += f" {note}"
            existing_note.assessment = assessment

            existing_note.save()
        else:
            note = record_integrity(db.session, DoctorNote,
                                    note=note,
                                    assessment=assessment,
                                    schedule=schedule
                                    )
            storage.save()

        return jsonify({'message': 'note successfuly updated'}), 201

    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        db.session.rollback()
        return {"error": "An unexpected error occurred.", "details": str(e)}
