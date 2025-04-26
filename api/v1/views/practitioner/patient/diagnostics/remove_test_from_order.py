from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.views.practitioner import practitioner
from api.v1.services.practitioner.patient.diagnostics.remove_test_from_order import (
    remove_test_from_order
)


@practitioner.route(
    '/patient/tests/<test_order_id>/remove/<diagnostic_test_id>', methods=['DELETE'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/diagnostics/remove_test.yml')
@jwt_required()
def pa_remove_test_from_order(test_order_id, diagnostic_test_id):
    return remove_test_from_order(test_order_id, diagnostic_test_id)
