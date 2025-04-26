"""
This module defines how to delete a test from a TestOrder
"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.diagnostics.order import TestOrder
from models.diagnostics.test import DiagnosticTest


def remove_test_from_order(test_order_id, diagnostic_test_id):
    """
    Remove a diagnostic test from a specific test order

    Args:
        test_order_id (str): ID of the test order
        diagnostic_test_id (str): ID of the diagnostic test to be removed

    Returns:
        tuple: response message and HTTP status code
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'message': 'user not found'}), 404

        if user.account_type != 'practitioner':
            return jsonify({'error': 'not authorised'}), 403

        test_order = storage.get(TestOrder, test_order_id)
        if not test_order:
            return jsonify({'error': 'test order not found'}), 404

        schedule = test_order.schedule
        if not schedule or schedule.appointment not in user.prac_profile.appointments:
            return jsonify({'error': 'not authorised for this schedule'}), 403

        test = DiagnosticTest.query.filter_by(id=diagnostic_test_id).first()
        if not test or test not in test_order.tests:
            return jsonify({'error': 'test not part of this order'}), 404

        test_order.tests.remove(test)
        storage.save()

        return jsonify({'message': 'test successfully removed from order'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
