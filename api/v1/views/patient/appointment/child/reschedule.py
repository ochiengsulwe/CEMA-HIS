from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.child.reschedule import (
        reschedule_appointment)

# Blueprint
from api.v1.views.patient import patient


@patient.route('/child/<child_id>/appointment/<schedule_id>/reschedule',
               methods=['PATCH'])
@swag_from('/api/v1/views/patient/documentation/appointment/child/reschedule.yml')
@jwt_required()
def reschedule_child_appointment(child_id, schedule_id):
    data = request.get_json()
    return reschedule_appointment(data, child_id, schedule_id)
