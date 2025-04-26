from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.prescription.child.all import all_prescriptions

# Blueprint
from api.v1.views.patient import patient


@patient.route('/<child_id>/prescriptions/all', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/prescription/child/all.yml')
@jwt_required()
def all_child_prescriptions(child_id):
    return all_prescriptions(child_id)
