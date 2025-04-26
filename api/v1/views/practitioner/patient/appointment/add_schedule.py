from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.appointment.add_schedule import (
    add_appointment_schedule)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/appointment/<appointment_id>/add-schedule',
                    methods=['POST'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/appointment/add_schedule.yml')
@jwt_required()
def schedule_add_pa(appointment_id):
    data = request.get_json()
    return add_appointment_schedule(data, appointment_id)
