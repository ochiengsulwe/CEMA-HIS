from flasgger.utils import swag_from

from flask import request, jsonify
from flask_login import login_required, current_user

from api.v1.views.auth import auth

from models import storage

# from utils.database import update_fields
# from utils.decorators import permission_required
from utils.general import data_check
# from utils.permissions import Permission


@auth.route('/register/adult', methods=['POST'])
@login_required
@swag_from('/api/v1/views/auth/documentation/register/adult.yml')
def adult_register():
    data = request.get_json()
    expected_fields = [
                        'middle_name', 'gender', 'date_of_birth',
                        'current_location'
                      ]

    if not current_user.is_authenticated and (
            current_user.account_type != 'practitioner'):
        return jsonify({'error': 'unauthorized'}), 403

    middle_name = data.get('middle_name')
    gender = data.get('gender')
    date_of_birth = data.get('date_of_birth')
    current_location = data.get('current_location')
    acc_status = 'verified'

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    error = data_check(data, expected_fields)
    if error:
        return error

    current_user.adult_profile.current_location = current_location
    current_user.user.gender = gender
    current_user.user.middle_name = middle_name
    current_user.user.date_of_birth = date_of_birth
    current_user.acc_status = acc_status

    storage.save()
    return jsonify({'message': 'Registered successfully.'}), 201
