from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.appointment.all_appointments import all_appointments

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/appointment/all', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/appointment/all.yml')
@jwt_required()
def all_pr_appointments():
    return all_appointments()
