from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.prescription.prescribe import (
    create_prescription)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/<schedule_id>/prescription/create', methods=['POST'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/prescription/prescribe.yml')
@jwt_required()
def create_pa_prescription(schedule_id):
    return create_prescription(schedule_id)
