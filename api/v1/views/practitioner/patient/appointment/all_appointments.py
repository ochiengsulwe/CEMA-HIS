from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.appointment.all import all_appointments

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/<loginfo_id>/appointment/all', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/patient/appointment/all.yml')
@jwt_required()
def all_pr_pa_appointments(loginfo_id):
    return all_appointments(loginfo_id)
