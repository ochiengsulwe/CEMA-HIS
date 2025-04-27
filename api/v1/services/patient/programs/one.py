"""
This module defines how a single health program can be retrieved by ID for practitioners
"""

from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.h_prog import HealthProgram


def get_program_by_id(program_id):
    """
        Retrieves a single health program by ID for an authenticated user.

        Args:
            program_id (str): The unique ID of the health program.

        Returns:
            tuple: response containing the program details or an error message.
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

        program = storage.get(HealthProgram, program_id)
        if not program:
            return jsonify({'error': 'health program not found'}), 404

        return jsonify({
            'id': program.id,
            'name': program.name,
            'description': program.description
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'database error', 'details': str(e)}), 500
