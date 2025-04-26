from flasgger.utils import swag_from
# from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.child.one_appointment import one_appointment

# Blueprint
from api.v1.views.patient import patient


@patient.route('/child/<child_id>/appointment/<appointment_id>', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/appointment/child/one.yml')
@jwt_required()
def one_child_appointment(appointment_id, child_id):
    return one_appointment(appointment_id, child_id)
