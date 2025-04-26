from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.prescription.child.one import get_prescription

# Blueprint
from api.v1.views.patient import patient


@patient.route('/<child_id>/prescriptions/<prescription_id>', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/prescription/child/one.yml')
@jwt_required()
def this_child_prescription(prescription_id, child_id):
    return get_prescription(prescription_id, child_id)
