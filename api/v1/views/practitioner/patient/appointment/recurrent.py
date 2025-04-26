from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.appointment.recurrent import repeat_appointment

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/appointment/<appointment_id>/mark-repeat',
                    methods=['PATCH'])
@swag_from('/api/v1/views/practitioner/documentation/patient/appointment/recurrent.yml')
@jwt_required()
def mark_pa_appointment_repeat(appointment_id):
    return repeat_appointment(appointment_id)
