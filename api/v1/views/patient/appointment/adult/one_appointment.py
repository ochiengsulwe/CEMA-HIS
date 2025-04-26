from flasgger.utils import swag_from
# from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.adult.one_appointment import one_appointment

# Blueprint
from api.v1.views.patient import patient


@patient.route('/appointment/<appointment_id>', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/appointment/adult/one.yml')
@jwt_required()
def one_adult_appointment(appointment_id):
    return one_appointment(appointment_id)
