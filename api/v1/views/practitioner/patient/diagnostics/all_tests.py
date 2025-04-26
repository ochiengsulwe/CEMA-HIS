from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.patient.diagnostics.test_list import (
    all_tests)

from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/tests/all', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/patient/diagnostics/all_tests.yml')
@jwt_required()
def pa_get_tests():
    return all_tests()
