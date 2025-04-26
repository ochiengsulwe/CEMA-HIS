from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.planner.span_info import span_info

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/planner/<slot_id>/<span_id>', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/planner/span_info.yml')
@jwt_required()
def practitioner_span_info(slot_id, span_id):
    return span_info(slot_id, span_id)
