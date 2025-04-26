from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.diagnosis.adult.one import get_specific_diagnosis

# Blueprint
from api.v1.views.patient import patient


@patient.route('/diagnoses/<diagnosis_id>', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/diagnosis/adult/one.yml')
@jwt_required()
def this_adult_diagnosis(diagnosis_id):
    return get_specific_diagnosis(diagnosis_id)
