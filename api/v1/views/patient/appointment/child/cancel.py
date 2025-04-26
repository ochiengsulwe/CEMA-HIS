from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.child.cancel import cancel_appointment

# Blueprint
from api.v1.views.patient import patient


@patient.route('/child/<child_id>/appointment/<schedule_id>/cancel', methods=['DELETE'])
@swag_from('/api/v1/views/patient/documentation/appointment/child/cancel.yml')
@jwt_required()
def cancel_child_appointment(child_id, schedule_id):
    return cancel_appointment(child_id, schedule_id)
