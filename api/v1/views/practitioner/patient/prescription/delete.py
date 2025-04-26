from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.prescription.delete import (
    delete_prescription_entry)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/prescription/<prescription_entry_id>/delete',
                    methods=['DELETE'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/prescription/delete.yml')
@jwt_required()
def delete_pres_entry(prescription_entry_id):
    return delete_prescription_entry(prescription_entry_id)
