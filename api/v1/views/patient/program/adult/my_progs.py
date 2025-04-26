from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.programs.adult.my_programs import list_enrolled_programs

# Blueprint
from api.v1.views.patient import patient


@patient.route('/programs/my-programs', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/program/adult/my_programs.yml')
@jwt_required()
def all_adult_programs():
    return list_enrolled_programs()
