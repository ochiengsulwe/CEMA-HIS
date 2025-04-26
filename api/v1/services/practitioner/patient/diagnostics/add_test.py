from flask import jsonify
from sqlalchemy.exc import IntegrityError

from api.v1 import db
from models import storage
from models.diagnostics.order import TestOrder
from models.diagnostics.test import DiagnosticTest
from models.diagnostics.link import TestOrderTestLink

from utils.database import record_integrity
from utils.general import data_check


def add_tests_to_order(test_order_id, data):
    """
    Add diagnostic tests to an existing TestOrder.

    Args:
        test_order_id (str): ID of the TestOrder.
        data (dict): Must contain a list of tests under the 'tests' key.
                     Each test must include 'test_id', and optionally 'status'.

    Returns:
        tuple: JSON response and HTTP status code
    """
    try:
        if not data or 'tests' not in data or not isinstance(data['tests'], list):
            return jsonify({'error': 'invalid entry'}), 400

        test_order = storage.get(TestOrder, test_order_id)
        if not test_order:
            return jsonify({'error': 'test order not found'}), 404

        for test_entry in data['tests']:
            required_fields = ['test_id']
            error_response = data_check(test_entry, required_fields)
            if error_response:
                return error_response

            test_id = test_entry.get('test_id')
            status = test_entry.get('status', 'waiting')

            diagnostic_test = storage.get(DiagnosticTest, test_id)
            if not diagnostic_test:
                return jsonify({'error': f'test with ID {test_id} not found'}), 404

            link = record_integrity(db.session, TestOrderTestLink,
                                    test_order=test_order,
                                    diagnostic_test=diagnostic_test,
                                    status=status)
            link.save()

        storage.save()
        return jsonify({'message': 'test(s) successfully added'}), 201

    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}, 500
    except Exception as e:
        db.session.rollback()
        return {"error": "Unexpected error occurred.", "details": str(e)}, 500
