from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.planner.create import practitioner_create_planner

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/planner/create', methods=['POST'])
@swag_from('/api/v1/views/practitioner/documentation/planner/create.yml')
@jwt_required()
def create_practitioner_planner():
    data = request.get_json()
    return practitioner_create_planner(data)
