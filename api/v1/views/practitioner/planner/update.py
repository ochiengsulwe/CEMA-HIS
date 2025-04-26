from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.planner.update import (
    practitioner_update_planner_time)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/planner/<span_id>/update', methods=['PATCH'])
@swag_from('/api/v1/views/practitioner/documentation/planner/update.yml')
@jwt_required()
def update_practitioner_planner(span_id):
    data = request.get_json()
    return practitioner_update_planner_time(data, span_id)
