from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.diagnosis.adult.all import all_diagnoses

# Blueprint
from api.v1.views.patient import patient


@patient.route('/diagnoses/all', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/diagnosis/adult/all.yml')
@jwt_required()
def all_adult_diagnoses():
    return all_diagnoses()
