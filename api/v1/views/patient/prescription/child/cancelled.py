from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.prescription.child.cancelled import cancelled_prescriptions

# Blueprint
from api.v1.views.patient import patient


@patient.route('/<child_id>/prescriptions/cancelled', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/prescription/child/cancelled.yml')
@jwt_required()
def all_cancelled_child_prescriptions(child_id):
    return cancelled_prescriptions(child_id)
