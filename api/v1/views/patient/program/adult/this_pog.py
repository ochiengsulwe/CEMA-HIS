from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.programs.adult.this_program import (
    retrieve_enrolled_program)

# Blueprint
from api.v1.views.patient import patient


@patient.route('/programs/<program_id>', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/program/adult/this_program.yml')
@jwt_required()
def this_adult_program(program_id):
    return retrieve_enrolled_program(program_id)
