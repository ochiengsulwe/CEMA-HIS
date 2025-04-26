from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.planner.clear_day import practitioner_clear_day

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/planner/<slot_id>/clear-day', methods=['DELETE'])
@swag_from('/api/v1/views/practitioner/documentation/planner/clear_day.yml')
@jwt_required()
def clear_practitioner_day(slot_id):
    return practitioner_clear_day(slot_id)
