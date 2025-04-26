from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.appointment.one_appointment import one_appointment

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/appointment/<appointment_id>', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/appointment/one.yml')
@jwt_required()
def one_pr_appointment(appointment_id):
    return one_appointment(appointment_id)
