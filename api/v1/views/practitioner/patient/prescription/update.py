from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.prescription.update import (
    update_frequency)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/prescription/<prescription_entry_id>/update',
                    methods=['PATCH'])
@swag_from(
    '/api/v1/views/practitioner/documentation/patient/prescription/update.yml')
@jwt_required()
def update_pres_entry(prescription_entry_id):
    data = request.get_json()
    return update_frequency(prescription_entry_id, data)
