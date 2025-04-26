from flasgger.utils import swag_from
# from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.general.prac_patient.schedule_dets import this_schedule

# Blueprint
from api.v1.views.patient import patient


@patient.route('/appointment/<schedule_id>', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/appointment/adult/schedule.yml')
@jwt_required()
def one_adult_schedule(schedule_id):
    return this_schedule(schedule_id)
