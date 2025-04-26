from flasgger.utils import swag_from
# from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.child.completed import completed_appointments

# Blueprint
from api.v1.views.patient import patient


@patient.route('/child/<child_id>/appointment/complete', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/appointment/child/completed.yml')
@jwt_required()
def complete_c_appointments(child_id):
    return completed_appointments(child_id)
