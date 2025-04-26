from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.prescription.child.issued import issued_prescriptions

# Blueprint
from api.v1.views.patient import patient


@patient.route('/<child_id>/prescriptions/issued', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/prescription/child/issued.yml')
@jwt_required()
def all_issued_child_prescriptions(child_id):
    return issued_prescriptions(child_id)
