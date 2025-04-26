from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.diagnosis.diagnose import (
    enter_diagnosis)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/<schedule_id>/diagnosis/create', methods=['POST'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/diagnosis/create.yml')
@jwt_required()
def pa_diagnose(schedule_id):
    data = request.get_json()
    return enter_diagnosis(data, schedule_id)
