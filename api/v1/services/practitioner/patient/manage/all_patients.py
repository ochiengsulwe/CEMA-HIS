"""
This module defines how all patients (both past and current) are retrieved

No filtering in this case, all of them are retrieved. A very expensive transaction.
"""
from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo


def all_patients():
    """
        Retrieves all patients for the authenticated practitioner.

        Returns:
            tuple: JSON response containing a dictionary of patient names and details,
               or an error message with appropriate status code.
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        if user.account_type == 'practitioner':
            appointments = user.prac_profile.appointments
            if not appointments:
                return jsonify({'error': 'no appointment yet'}), 404

            patients_by_name = defaultdict(list)
            for appointment in appointments:
                if appointment.adult_profile is not None:
                    identity = appointment.adult_profile.identity
                    profile = appointment.adult_profile.loginfo
                elif appointment.child_profile is not None:
                    identity = appointment.child_profile.identity
                    profile = appointment.child_profile.loginfo
                else:
                    return jsonify({'error': 'not authorised'}), 403

                first_name = identity.first_name
                middle_name = identity.middle_name
                last_name = identity.last_name
                name = " ".join(filter(None, [first_name, middle_name, last_name]))

                patient_details = {
                    "age": str(identity.age),
                    "gender": identity.gender,
                    "loginfo_id": profile.id,
                    "type": profile.account_type,
                    "program_in": appointment.program.name
                }
                patients_by_name[name].append(patient_details)

            return jsonify(patients_by_name), 200
        else:
            return jsonify({'error': 'not authorised'}), 403
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
