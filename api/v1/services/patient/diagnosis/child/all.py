"""
This module defines how all diagnoses will be retrieved for dependents only.

No filtering in this case, all of them are retrieved. A very expensive transaction.
"""
from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.child_profile import ChildProfile
from models.loginfo import LogInfo
from utils.support import is_parent


def all_diagnoses(child_id):
    """
        Retrieves all diagnoses for a child via an authenticated parent's account.

        Args:
            child_id (str): A child's ID which retrieves from ChildProfile table

        Returns:
            tuple: response containing a list of diagnoses or an error message, and
                associated HTTP response code
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        child = storage.get(ChildProfile, child_id)
        if not child:
            return jsonify({'error': 'child not found'}), 404

        if not is_parent(child, user):
            return jsonify({'error': 'not authorised'}), 403

        diagnoses_by_date = defaultdict(list)

        for appointment in child.appointments:
            for schedule in appointment.schedules:
                if schedule.diagnosis:
                    diagnosis = schedule.diagnosis
                    practitioner = (appointment.practitioner.identity if
                                    appointment.practitioner else None)
                    full_name = " ".join(
                        filter(
                            None, [practitioner.first_name, practitioner.middle_name,
                                   practitioner.last_name]
                        )
                    ) if practitioner else None

                    diagnosis_details = {
                        "diagnosis": diagnosis.diagnosis,
                        "severity": diagnosis.severity,
                        "prognosis": diagnosis.prognosis,
                        "diagnosed_by": full_name,
                        "schedule_id": schedule.id,
                        "appointment_id": appointment.id,
                        "created_at": diagnosis.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    }

                    diagnosis_date = diagnosis.created_at.strftime('%Y-%m-%d')
                    diagnoses_by_date[diagnosis_date].append(diagnosis_details)

        return jsonify(diagnoses_by_date), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
