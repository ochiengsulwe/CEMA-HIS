from flasgger.utils import swag_from
# from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.child.all_appointments import all_appointments

# Blueprint
from api.v1.views.patient import patient


@patient.route('/child/<child_id>/appointment/all', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/appointment/child/all.yml')
@jwt_required()
def all_child_appointments(child_id):
    return all_appointments(child_id)
