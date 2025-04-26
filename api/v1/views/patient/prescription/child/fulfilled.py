from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.prescription.child.fulfilled import (
    fulfilled_prescriptions)

# Blueprint
from api.v1.views.patient import patient


@patient.route('/<child_id>/prescriptions/fulfilled', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/prescription/child/fulfilled.yml')
@jwt_required()
def all_fulfilled_child_prescriptions(child_id):
    return fulfilled_prescriptions(child_id)
