from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.prescription.adult.cancelled import cancelled_prescriptions

# Blueprint
from api.v1.views.patient import patient


@patient.route('/prescriptions/cancelled', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/prescription/adult/cancelled.yml')
@jwt_required()
def all_cancelled_adult_prescriptions():
    return cancelled_prescriptions()
