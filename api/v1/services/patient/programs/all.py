"""
This module defines how all health programs will be retrieved for practitioners.

No filtering in this case, all of them are retrieved. A very expensive transaction.
"""
from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.h_prog import HealthProgram
from models.loginfo import LogInfo


def all_programs():
    """
        Retrieves all available health programs in the system.

        Returns:
            tuple: response containing a list of programs or an error message.
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        if (user.account_type == 'practitioner' or user.account_type == 'adult'):
            programs = storage.all(HealthProgram)
            grouped_programs = defaultdict(list)
            for program in programs:
                grouped_programs[program.name].append({
                    'id': program.id,
                    'description': program.description
                })

            grouped_programs = dict(grouped_programs)

            return jsonify(grouped_programs), 200
        else:
            return jsonify({'error': 'not authorised'}), 403

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'database error', 'details': str(e)}), 500
