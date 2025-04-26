from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required
from api.v1.services.patient.prescription.adult.one import get_prescription

# Blueprint
from api.v1.views.patient import patient


@patient.route('/prescriptions/<prescription_id>', methods=['GET'])
@swag_from('/api/v1/views/patient/documentation/prescription/adult/one.yml')
@jwt_required()
def this_adult_prescription(prescription_id):
    return get_prescription(prescription_id)
