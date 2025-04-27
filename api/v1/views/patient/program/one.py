from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.v1.services.patient.programs.one import get_program_by_id

# Blueprint
from api.v1.views.patient import patient


@patient.route('/programs/<program_id>', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/program/one.yml')
@jwt_required()
def program_for_patient(program_id):
    return get_program_by_id(program_id)
