from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.programs.create import create_practitioner_program

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/programs/<program_id>/create', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/programs/create.yml')
@jwt_required()
def create_program(program_id):
    return create_practitioner_program(program_id)
