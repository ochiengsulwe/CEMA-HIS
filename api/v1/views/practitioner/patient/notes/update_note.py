from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.notes.update_note import (
    update_note)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/notes/update/<schedule_id>', methods=['PATCH'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/notes/update.yml')
@jwt_required()
def pa_update_note(schedule_id):
    data = request.get_json()
    return update_note(data, schedule_id)
