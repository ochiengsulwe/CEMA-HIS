from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.find_program_pracs import (
    practitioners_by_program)

# Blueprint
from api.v1.views.patient import patient


@patient.route('/programs/<program_id>/practitioners/all', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/appointment/all_pracs.yml')
@jwt_required()
def all_pracs_in_program(program_id):
    return practitioners_by_program(program_id)
