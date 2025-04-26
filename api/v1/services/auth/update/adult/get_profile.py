from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from models.loginfo import LogInfo


@jwt_required()
# @auth.route('/profile', methods=['GET'])
# @login_required
@swag_from('/api/v1/views/auth/documentation/update/get_profile.yml')
def get_adult_profile():
    current_user_id = get_jwt_identity()
    current_user = LogInfo.query.get(current_user_id)
    if not current_user_id or current_user.account_type != 'adult':
        return jsonify({'error': 'unauthorized'}), 403

    profile_data = {
        'birth_cert_number': current_user.user.birth_cert_number,
        'passport_number': current_user.user.passport_number,
        'permanent_location': current_user.adult_profile.permanent_location,
    }
    return jsonify(profile_data), 200
