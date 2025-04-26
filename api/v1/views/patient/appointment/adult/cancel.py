from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.adult.cancel import cancel_appointment

# Blueprint
from api.v1.views.patient import patient


@patient.route('/appointment/cancel/<schedule_id>', methods=['DELETE'])
@swag_from('/api/v1/views/patient/documentation/appointment/adult/cancel.yml')
@jwt_required()
def cancel_adult_appointment(schedule_id):
    return cancel_appointment(schedule_id)
