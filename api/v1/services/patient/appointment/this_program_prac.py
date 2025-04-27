"""
This module defines how to retrieve details of a specific practitioner enrolled in a
    program.

"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.practitioner_profile import PracProfile
from models.loginfo import LogInfo


def specific_practitioner(practitioner_id):
    """
        Retrieves details of a specific practitioner by ID.

        Args:
            practitioner_id (str): the specific practitioner

        Returns:
            tuple: response containing practitioner details or an error message, and
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

        practitioner = storage.get(PracProfile, practitioner_id)
        if not practitioner:
            return jsonify({'error': 'practitioner not found'}), 404

        identity = practitioner.identity
        name = " ".join(filter(None,
                               [identity.first_name,
                                identity.middle_name,
                                identity.last_name
                                ]
                               )
                        )

        practitioner_details = {
            "practitioner_id": practitioner.id,
            "name": name,
            "cost": practitioner.fee,
            "profession": practitioner.profession,
        }

        # Only add 'specialization' if it's not None
        if practitioner.specialization:
            practitioner_details["specialization"] = practitioner.specialization

        return jsonify(practitioner_details), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
