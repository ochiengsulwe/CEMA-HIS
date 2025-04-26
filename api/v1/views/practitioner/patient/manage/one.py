from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.manage.this_patient import this_patient

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/<loginfo_id>', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/patient/manage/one.yml')
@jwt_required()
def one_pr_patient(loginfo_id):
    return this_patient(loginfo_id)
