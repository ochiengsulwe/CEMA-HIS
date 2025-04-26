from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.practitioner.patient.appointment.one import patient_appointment

# Blueprint
from api.v1.views.practitioner import practitioner


@practitioner.route('/patient/appointment/<schedule_id>', methods=['GET'])
@swag_from('/api/v1/views/practitioner/documentation/patient/appointment/one.yml')
@jwt_required()
def this_patient_appointment(schedule_id):
    return patient_appointment(schedule_id)
