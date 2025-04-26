from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.patient.diagnostics.this_test import (
    this_test)

from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/tests/<diagnostic_test_id>', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/patient/diagnostics/get_test.yml')
@jwt_required()
def pa_get_test(diagnostic_test_id):
    return this_test(diagnostic_test_id)
