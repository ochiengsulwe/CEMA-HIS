from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.prescription.adult.fulfilled import fulfilled_prescriptions

# Blueprint
from api.v1.views.patient import patient


@patient.route('/prescriptions/fulfilled', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/prescription/adult/fulfilled.yml')
@jwt_required()
def all_fulfilled_adult_prescriptions():
    return fulfilled_prescriptions()
