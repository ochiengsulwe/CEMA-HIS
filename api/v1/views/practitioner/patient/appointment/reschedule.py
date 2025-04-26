from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.appointment.reschedule import (
    reschedule_appointment)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/appointment/<schedule_id>/reschedule', methods=['PATCH'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/appointment/reschedule.yml')
@jwt_required()
def reschedule_pn_pa_appointment(schedule_id):
    data = request.get_json()
    return reschedule_appointment(data, schedule_id)
