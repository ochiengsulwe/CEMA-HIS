from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.prescription.issue import (
    issue_prescription)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/<prescription_id>/issue', methods=['PATCH'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/prescription/issue.yml')
@jwt_required()
def issue_pa_prescription(prescription_id):
    return issue_prescription(prescription_id)
