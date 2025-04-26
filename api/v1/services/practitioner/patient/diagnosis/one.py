"""
The module returns diagnosis information of a specific schedule
"""
from flask import jsonify

from flask_jwt_extended import get_jwt_identity

from sqlalchemy.exc import IntegrityError

from api.v1 import db

from models import storage
from models.diagnosis import Diagnosis
from models.loginfo import LogInfo
from models.schedule import Schedule


def this_diagnosis(schedule_id):
    """
    Retrieves diagnosis information of an appointment schedule in-place

    Args:
        schedule_id (str): unique appointment-in-place identifier

    Returns:
        tuple: message (diagnosis info or error), coupled with a matching HTTP
            response code.
    """
    try:
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

        diagnosis = Diagnosis.query.filter_by(schedule_id=schedule.id).first()
        if not diagnosis:
            return jsonify({'error': 'diagnosis not found'}), 404
        d = f"{diagnosis.severity} {diagnosis.diagnosis}"
        info = {
            "entered_on": diagnosis.updated_at.strftime('%Y-%m-%d'),
            "entered_at": diagnosis.updated_at.strftime('%H:%M'),
            "on_day": diagnosis.updated_at.strftime('%A'),
            "diagnosis": d,
            "prognosis": diagnosis.prognosis
        }
        return jsonify(info), 200

    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        db.session.rollback()
        return {"error": "An unexpected error occurred.", "details": str(e)}
