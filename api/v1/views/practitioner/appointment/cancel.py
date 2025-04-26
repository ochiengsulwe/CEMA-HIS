from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.appointment.cancel import cancel_appointment

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/appointment/<schedule_id>/cancel', methods=['DELETE'])
@swag_from('/api/v1/views/practitioner/documentation/appointment/cancel.yml')
@jwt_required()
def cancel_pnt_appointment(schedule_id):
    return cancel_appointment(schedule_id)
