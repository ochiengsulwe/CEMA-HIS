from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.planner.day_info import day_info

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/planner/<slot_id>', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/planner/day_info.yml')
@jwt_required()
def practitioner_day_info(slot_id):
    return day_info(slot_id)
