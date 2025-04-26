from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.schedule import Schedule


def all_diagnoses():
    """
    Retrieves all diagnoses for the authenticated adult user, grouped by date.

    Returns:
        tuple: response containing a list of diagnoses or an error message,
        and associated HTTP response code
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
        if not appointments:
            return jsonify({'message': 'no appointments found'}), 404

        schedules = Schedule.query.filter(
            Schedule.appointment_id.in_([appt.id for appt in appointments])
        ).all()

        diagnoses_by_date = defaultdict(list)

        for schedule in schedules:
            if schedule.diagnosis:
                diagnosis_entry = schedule.diagnosis

                practitioner_name = schedule.appointment.practitioner.identity
                full_name = " ".join(filter(None, [
                    practitioner_name.first_name,
                    practitioner_name.middle_name,
                    practitioner_name.last_name
                ]))

                diagnosis_details = {
                    "diagnosis": diagnosis_entry.diagnosis,
                    "severity": diagnosis_entry.severity,
                    "prognosis": diagnosis_entry.prognosis,
                    "diagnosed_by": full_name,
                    "schedule_id": schedule.id,
                    "appointment_id": schedule.appointment_id
                }

                diagnoses_by_date[schedule.date.strftime('%Y-%m-%d')].append(
                    diagnosis_details)

        if not diagnoses_by_date:
            return jsonify({'message': 'no diagnoses found'}), 404

        return jsonify(diagnoses_by_date), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
