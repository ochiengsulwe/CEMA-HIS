from flasgger.utils import swag_from

from flask import request, jsonify
from flask_login import login_required, current_user

# from api.v1 import db
from api.v1.views.auth import auth

from models import storage

from utils.general import verify_data


@auth.route('/update/practitioner', methods=['POST'])
@login_required
@swag_from('/api/v1/views/auth/documentation/update/practitioner.yml')
def practitioner_update():
    data = request.get_json()
    expected_fields = ['fee', 'location', 'bio']

    if not current_user.is_authenticated or (
            current_user.account_type != 'practitioner'):
        return jsonify({'error': 'unauthorized'}), 403

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    verify_data(data, expected_fields)

    bio = data.get('bio')
    fee = data.get('fee')
    location = data.get('location')

    if 'location' in data:
        current_user.prac_profile.location = location
    if 'fee' in data:
        current_user.prac_profile.fee = fee
    if 'bio' in data:
        current_user.prac_profile.bio = bio
    storage.save()
    return jsonify({'message': 'successfully updated'}), 201
