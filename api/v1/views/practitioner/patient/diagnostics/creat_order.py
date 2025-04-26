from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.patient.diagnostics.create_test_order import (
    create_test_order)

from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/<schedule_id>/test-order/create', methods=['POST'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/diagnostics/create_order.yml')
@jwt_required()
def pa_create_order(schedule_id):
    return create_test_order(schedule_id)
