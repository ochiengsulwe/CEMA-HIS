from flasgger.utils import swag_from
# from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.adult.all_appointments import all_appointments

# Blueprint
from api.v1.views.patient import patient


@patient.route('/appointment/all', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/appointment/adult/all.yml')
@jwt_required()
def all_adult_appointments():
    return all_appointments()
