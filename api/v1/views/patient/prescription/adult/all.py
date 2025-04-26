from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.prescription.adult.all import all_prescriptions

# Blueprint
from api.v1.views.patient import patient


@patient.route('/prescriptions/all', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/prescription/adult/all.yml')
@jwt_required()
def all_adult_prescriptions():
    return all_prescriptions()
