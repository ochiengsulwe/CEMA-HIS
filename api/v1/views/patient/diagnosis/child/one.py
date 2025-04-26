from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.diagnosis.child.one import retrieve_child_diagnosis

# Blueprint
from api.v1.views.patient import patient


@patient.route('/<child_id>/diagnoses/<diagnosis_id>', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/diagnosis/child/one.yml')
@jwt_required()
def this_child_diagnosis(child_id, diagnosis_id):
    return retrieve_child_diagnosis(child_id, diagnosis_id)
