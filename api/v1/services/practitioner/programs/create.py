from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.h_prog import HealthProgram
from models.prac_program import PractitionerProgram


def create_practitioner_program(program_id):
    """
        Links a practitioner to a health program (or multiple programs).

        Args:
            program_id (str): the program unique identifier

        Returns:
            tuple: response with success message or error.
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user or user.account_type != 'practitioner':
            return jsonify({'error': 'not authorised'}), 403

        prac = user.prac_profile
        if not prac:
            return jsonify({'error': 'practitioner profile not found'}), 404

        program = storage.get(HealthProgram, program_id)
        if not program:
            return jsonify({'error': 'Program not found'}), 404

        existing = PractitionerProgram.query.filter_by(
            prac_id=prac.id, program_id=program_id).first()
        if existing:
            return jsonify({'error': 'Program already linked'}), 409

        new_link = PractitionerProgram(prac_id=prac.id, program_id=program_id)
        db.session.add(new_link)
        db.session.commit()

        return jsonify(
            {'message': f'Successfuly created  program [{program.name}]'}
        ), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'database error', 'details': str(e)}), 500
