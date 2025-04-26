from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.programs.child.this_program import (
    retrieve_enrolled_program)

# Blueprint
from api.v1.views.patient import patient


@patient.route('/<child_id>/programs/<program_id>', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/program/child/this_program.yml')
@jwt_required()
def this_child_program(program_id, child_id):
    return retrieve_enrolled_program(program_id, child_id)
