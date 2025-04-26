from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.planner.spans import days_spans

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/planner/<slot_id>/spans', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/planner/spans.yml')
@jwt_required()
def retrieve_days_spans(slot_id):
    return days_spans(slot_id)
