from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.prescription.child.received import received_prescriptions

# Blueprint
from api.v1.views.patient import patient


@patient.route('/<child_id>/prescriptions/received', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/prescription/child/received.yml')
@jwt_required()
def all_received_child_prescriptions(child_id):
    return received_prescriptions(child_id)
