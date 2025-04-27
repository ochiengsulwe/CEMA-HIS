from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.this_program_prac import specific_practitioner

# Blueprint
from api.v1.views.patient import patient


@patient.route('/programs/<practitioner_id>', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/appointment/this_prac.yml')
@jwt_required()
def program_practitioner(practitioner_id):
    return specific_practitioner(practitioner_id)
