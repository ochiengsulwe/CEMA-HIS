from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.notes.create_note import (
    create_notes)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/notes/create/<schedule_id>', methods=['POST'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/notes/create.yml')
@jwt_required()
def pa_create_note(schedule_id):
    data = request.get_json()
    return create_notes(data, schedule_id)
