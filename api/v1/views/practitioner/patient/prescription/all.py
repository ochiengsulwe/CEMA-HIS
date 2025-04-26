from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.prescription.get_all import (
    get_prescription_entries)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/<prescription_id>/all', methods=['GET'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/prescription/all.yml')
@jwt_required()
def get_prescriptions(prescription_id):
    return get_prescription_entries(prescription_id)
