from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.planner.delete_span import practitioner_delete_span

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/planner/<span_id>/delete', methods=['DELETE'])
@swag_from('/api/v1/views/practitioner/documentation/planner/delete_span.yml')
@jwt_required()
def delete_practitioner_span(span_id):
    return practitioner_delete_span(span_id)
