from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.appointment.pending import (
    pending_appointments)

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/<loginfo_id>/appointment/upcoming', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/patient/appointment/pending.yml')
@jwt_required()
def pending_pr_pa_appointments(loginfo_id):
    return pending_appointments(loginfo_id)
