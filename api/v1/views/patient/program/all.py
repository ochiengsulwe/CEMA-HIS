from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.practitioner.programs.all import all_programs

# Blueprint
from api.v1.views.patient import patient


@patient.route('/programs/available', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/program/all.yml')
@jwt_required()
def retrieve_for_patient_programs():
    return all_programs()
