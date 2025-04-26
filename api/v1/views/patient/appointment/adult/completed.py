from flasgger.utils import swag_from
# from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.adult.completed import completed_appointments

# Blueprint
from api.v1.views.patient import patient


@patient.route('/appointment/complete', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/appointment/adult/completed.yml')
@jwt_required()
def complete_appointments():
    return completed_appointments()
