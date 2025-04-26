from flask import request, jsonify
# from flasgger.utils import swag_from

from api.v1 import db
from api.v1.views.unit.general import facility

from models import storage
from models.facilities.ambulance import Ambulance
from models.facilities.hospital import Hospital
from models.facilities.lab import Lab
from models.facilities.pharmacy import Pharmacy
from models.proxy.facilities.ambulance import ProxyAmbulance
from models.proxy.facilities.hospital import ProxyHospital
from models.proxy.facilities.lab import ProxyLaboratory
from models.proxy.facilities.pharmacy import ProxyPharmacy

from utils.database import record_integrity
from utils.general import data_check


@facility.route('/register_facility', methods=['POST'])
# @swag_from('/api/v1/views/unit/general/documentation/register_facility.yml')
def register_facility():
    data = request.get_json()
    required_fields = [
                'email', 'password', 'facility_type',
                'registration_number'
    ]
    facilities = {
        "ProxyAmbulance": ProxyAmbulance, "ProxyHospital": ProxyHospital,
        "ProxyLaboratory": ProxyLaboratory, "ProxyPharmacy": ProxyPharmacy
    }

    facilities_ = {
        "Ambulance": Ambulance, "Hospital": Hospital,
        "Lab": Lab, "Pharmacy": Pharmacy
    }
    if not data:
        return jsonify({'message': 'invalid data provided!'}), 400

    error_response = data_check(data, required_fields)
    if error_response:
        return error_response
    email = data.get('email')
    # password = data.get('password')
    facility_type = data.get('facility_type')
    registration_number = data.get('registration_number')
    fac = f"Proxy{facility_type}"
    facility = facilities.get(fac)
    if not facility:
        return jsonify(
                {'error': f"The facility type {facility_type} is not valid"}
                ), 400

    """Querying third party database to check if facility is
    registered with their associated registering body."""
    new_unit = db.session.query(facility).filter(
                                facility.registration_number == registration_number
                                ).first()
    if new_unit:
        """Check if facility is already registered with us"""
        facility_ = facility_type
        if facility_ not in facilities_:
            return jsonify({"message": "invalid facility"}), 404
        facility_model = facilities_[facility_type]
        present = db.session.query(facility_model).filter(
                facility_model.licence_number == new_unit.registration_number).first()
        if present:
            msg = f"{present.name} has an existiing account."
            return jsonify({'message': msg}), 409
        """ check if email of registration match with the provided one"""
        if email != new_unit.email:
            err = 'Please provide the email address used to register ' + \
                  f'{new_unit.name} with the National Registration Body'
            return jsonify({'error': err}), 401

        error_response = data_check(data, required_fields)
        if error_response:
            return error_response

        try:
            new_facility = record_integrity(db.session, facility_model,
                                            name=new_unit.name,
                                            licence_number=new_unit.registration_number)

        except ValueError as e:
            return jsonify({'error': str(e)}), 409

        storage.new(new_facility)
        storage.save()

        response_data = new_facility.to_dict()
        mess = f'account for ({new_facility.name}) was created successfully'
        response_data['message'] = mess
        return jsonify(response_data), 201
