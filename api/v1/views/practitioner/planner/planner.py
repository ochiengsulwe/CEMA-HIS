from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.planner.planner import planner

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/planner', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/planner/planner.yml')
@jwt_required()
def retrieve_practitioner_planner():
    return planner()
