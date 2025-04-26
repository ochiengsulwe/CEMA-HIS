from flasgger.utils import swag_from
# from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.child.upcoming import upcoming_appointments

# Blueprint
from api.v1.views.patient import patient


@patient.route('/child/<child_id>/appointment/upcoming', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/appointment/child/upcoming.yml')
@jwt_required()
def upcoming_c_appointment(child_id):
    return upcoming_appointments(child_id)
