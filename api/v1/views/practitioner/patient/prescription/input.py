from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.prescription.input_prescriptions import (
    enter_prescription)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/<prescription_id>/create', methods=['POST'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/prescription/input.yml')
@jwt_required()
def enter_pa_prescriptions(prescription_id):
    data = request.get_json()
    return enter_prescription(data, prescription_id)
