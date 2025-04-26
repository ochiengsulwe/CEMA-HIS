from flasgger.utils import swag_from
# from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.child.schedule import this_child_schedule

# Blueprint
from api.v1.views.patient import patient


@patient.route('/child/<child_id>/appointment/<schedule_id>', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/appointment/child/schedule.yml')
@jwt_required()
def one_child_schedule(schedule_id, child_id):
    return this_child_schedule(schedule_id, child_id)
