from flasgger.utils import swag_from
# from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.adult.upcoming import upcoming_appointments

# Blueprint
from api.v1.views.patient import patient


@patient.route('/appointment/upcoming', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/appointment/adult/upcoming.yml')
@jwt_required()
def upcoming_appointment():
    return upcoming_appointments()
