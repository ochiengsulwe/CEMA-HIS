from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.appointment.upcoming import pending_appointments

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/appointment/upcoming', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/appointment/upcoming.yml')
@jwt_required()
def appointments_upcoming():
    return pending_appointments()
