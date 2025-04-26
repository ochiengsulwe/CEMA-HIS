"""
This module defines how all tests available will be retrieved
"""
from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.diagnostics.test import DiagnosticTest


def all_tests():
    """
        Retrieves all tests available in the system.

        Returns:
            tuple: response containing a list of tests grouped by category or an error
                message.
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

        tests = db.session.query(DiagnosticTest).all()
        if not tests:
            return jsonify({'error': 'tests not found'}), 404

        tests_by_category = defaultdict(list)
        for test in tests:
            test_details = {
                "test_id": test.id,
                "test_name": test.name,
                "test_for": test.test_for
            }
            tests_by_category[test.category.name].append(test_details)

        return jsonify(tests_by_category), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
