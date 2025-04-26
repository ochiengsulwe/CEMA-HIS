from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.adult.reschedule import (
        reschedule_appointment)

# Blueprint
from api.v1.views.patient import patient


@patient.route('/appointment/<schedule_id>/reschedule', methods=['PATCH'])
@swag_from('/api/v1/views/patient/documentation/appointment/adult/reschedule.yml')
@jwt_required()
def reschedule_adult_appointment(schedule_id):
    data = request.get_json()
    return reschedule_appointment(data, schedule_id)
