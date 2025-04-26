from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.manage.all_patients import all_patients

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/all', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/patient/manage/all.yml')
@jwt_required()
def all_pr_patients():
    return all_patients()
