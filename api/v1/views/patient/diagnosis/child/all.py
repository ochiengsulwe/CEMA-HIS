from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.diagnosis.child.all import all_diagnoses

# Blueprint
from api.v1.views.patient import patient


@patient.route('/<child_id>/diagnoses/all', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/diagnosis/child/all.yml')
@jwt_required()
def all_child_diagnoses(child_id):
    return all_diagnoses(child_id)
