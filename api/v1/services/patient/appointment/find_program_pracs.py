"""
This module defines how all practitioners connected to a program will be retrieved for
    authenticated adults only.
"""

from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.prac_program import PractitionerProgram


def practitioners_by_program(program_id):
    """
        Retrieves all practitioners linked to a specific program for authenticated
            adult users.

        Args:
            program_id (str): ID of the health program.

        Returns:
            tuple: response containing a list of practitioners or an error message, and
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

        prac_programs = PractitionerProgram.query.filter_by(program_id=program_id).all()

        practitioners_by_name = defaultdict(dict)
        for pp in prac_programs:
            practitioner = pp.practitioner

            if practitioner and practitioner.identity:
                identity = practitioner.identity
                first_name = identity.first_name
                middle_name = identity.middle_name
                last_name = identity.last_name
                name = " ".join(filter(None, [first_name, middle_name, last_name]))

                practitioners_by_name[name] = {
                    "cost": practitioner.fee,
                    "profession": practitioner.profession,
                    "practitioner_id": practitioner.id
                }

                if practitioner.specialization:
                    practitioners_by_name[name]["specialization"] = (
                        practitioner.specialization)

        return jsonify(practitioners_by_name), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
