from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.prescription.adult.issued import issued_prescriptions

# Blueprint
from api.v1.views.patient import patient


@patient.route('/prescriptions/issued', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/prescription/adult/issued.yml')
@jwt_required()
def all_issued_adult_prescriptions():
    return issued_prescriptions()
