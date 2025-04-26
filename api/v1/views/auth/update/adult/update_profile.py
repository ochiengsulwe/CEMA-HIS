from flasgger.utils import swag_from

from flask import request, jsonify
from flask_login import login_required, current_user

from api.v1.views.auth import auth

from models import storage

from utils.general import verify_data


# @jwt_required()
@auth.route('/update/adult', methods=['POST'])
@login_required
@swag_from('/api/v1/views/auth/documentation/update/adult.yml')
def adult_update():
    data = request.get_json()
    expected_fields = [
                        'birth_cert_number', 'passport_number',
                        'parmanent_location'
                      ]

    if not current_user.is_authenticated or current_user.account_type != 'adult':
        return jsonify({'error': 'unauthorized'}), 403

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    verify_data(data, expected_fields)

    birth_cert_number = data.get('birth_cert_number')
    passport_number = data.get('passport_number')
    parmanent_location = data.get('parmanent_location')

    if 'parmanent_location' in data:
        current_user.adult_profile.parmanent_location = parmanent_location
    if 'passport_number' in data:
        current_user.user.passport_number = passport_number
    if 'birth_cert_number' in data:
        current_user.user.birth_cert_number = birth_cert_number
    storage.save()
    return jsonify({'message': 'successfully updated'}), 201
