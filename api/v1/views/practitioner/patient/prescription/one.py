from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.prescription.get_one import (
    get_prescription_entry_details)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/prescription/<prescription_entry_id>', methods=['GET'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/prescription/one.yml')
@jwt_required()
def get_entry_info(prescription_entry_id):
    return get_prescription_entry_details(prescription_entry_id)
