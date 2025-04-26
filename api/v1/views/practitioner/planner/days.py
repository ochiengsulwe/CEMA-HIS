from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.planner.days import get_available_days

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/planner/available-days', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/planner/days.yml')
@jwt_required()
def retrieve_practitioner_days():
    return get_available_days()
