from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.diagnosis.one import (
    this_diagnosis)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/<schedule_id>/diagnosis', methods=['GET'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/diagnosis/one.yml')
@jwt_required()
def retrieve_diagnosis(schedule_id):
    return this_diagnosis(schedule_id)
