"""
This module defines how a specific test info is to be retrieved
"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.diagnostics.test import DiagnosticTest


def this_test(diagnostic_test_id):
    """
        Retrieves a single diagnostic test information

        Returns:
            tuple: response containing test info or an error message.
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'mesasge': 'user not found'}), 404

        if user.account_type != 'practitioner':
            return jsonify({'error': 'not authorised'}), 403

        test = DiagnosticTest.query.filter_by(id=diagnostic_test_id).first()
        if not test:
            return jsonify({'error': 'test not found'}), 404

        test_details = {
            "test_id": test.id,
            "test_name": test.name,
            "test_for": test.test_for
        }
        return jsonify(test_details), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
