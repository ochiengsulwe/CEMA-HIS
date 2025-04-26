from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.patient.diagnostics.add_test import (
    add_tests_to_order)

from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/test-order/<test_order_id>/add-tests', methods=['POST'])
@swag_from('/api/v1/views/practitioner/documentation/patient/diagnostics/add_test.yml')
@jwt_required()
def pa_add_tests_to_order(test_order_id):
    data = request.get_json()
    return add_tests_to_order(test_order_id, data)
