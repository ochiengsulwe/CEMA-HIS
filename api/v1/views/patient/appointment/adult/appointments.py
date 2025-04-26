from flasgger.utils import swag_from
# from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.adult.appointments import appointments

# Blueprint
from api.v1.views.patient import patient


@patient.route('/appointments/', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/appointment/adult/appointments.yml')
@jwt_required()
def adult_appointments():
    return appointments()
