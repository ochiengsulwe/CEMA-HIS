from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.programs.one import get_program_by_id

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/programs/<program_id>', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/programs/one.yml')
@jwt_required()
def this_program(program_id):
    return get_program_by_id()
