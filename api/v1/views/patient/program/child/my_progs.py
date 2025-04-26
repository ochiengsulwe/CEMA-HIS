from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.programs.child.my_programs import list_enrolled_programs

# Blueprint
from api.v1.views.patient import patient


@patient.route('/<child_id>/programs/my-programs', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/program/child/my_programs.yml')
@jwt_required()
def all_child_programs(child_id):
    return list_enrolled_programs(child_id)
