from flask import jsonify
from flask_login import login_required, current_user
# from flasgger import swag_from


# @auth.route('/profile', methods=['GET'])
@login_required
def get_profile():
    if not current_user.is_authenticated or current_user.account_type != 'adult':
        return jsonify({'error': 'unauthorized'}), 403

    profile_data = {
        'birth_cert_number': current_user.user.birth_cert_number,
        'passport_number': current_user.user.passport_number,
        'permanent_location': current_user.adult_profile.permanent_location,
        'bio': current_user.adult_profile.bio
    }

    return jsonify(profile_data), 200
