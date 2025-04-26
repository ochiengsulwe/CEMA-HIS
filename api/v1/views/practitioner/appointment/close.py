from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.appointment.close import end_appointment

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/appointment/<appointment_id>/close', methods=['DELETE'])
@swag_from('/api/v1/views/practitioner/documentation/appointment/close.yml')
@jwt_required()
def prac_end_appointment(appointment_id):
    return end_appointment(appointment_id)
