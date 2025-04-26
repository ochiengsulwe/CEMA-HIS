from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.appointment.complete import (
    complete_appointments)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/<loginfo_id>/appointment/complete', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/patient/appointment/completed.yml')
@jwt_required()
def complete_pr_pa_appointments(loginfo_id):
    return complete_appointments(loginfo_id)
