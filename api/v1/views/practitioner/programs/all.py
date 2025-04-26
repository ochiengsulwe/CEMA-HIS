from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.programs.all import all_programs

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/programs/all', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/programs/all.yml')
@jwt_required()
def retrieve_programs():
    return all_programs()
