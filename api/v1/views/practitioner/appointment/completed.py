from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.appointment.completed import completed_appointments

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/appointment/complete', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/appointment/completed.yml')
@jwt_required()
def appointments_completed():
    return completed_appointments()
