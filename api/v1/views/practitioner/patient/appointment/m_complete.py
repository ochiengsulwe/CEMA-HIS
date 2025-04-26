from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.appointment.complete import complete_appointment

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/appointment/<schedule_id>/mark-complete',
                    methods=['PATCH'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/appointment/m_complete.yml')
@jwt_required()
def mark_pa_appointment_complete(schedule_id):
    return complete_appointment(schedule_id)
