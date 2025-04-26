"""
Logs out any signed in user
"""
from flasgger.utils import swag_from
from api.v1.views.auth import auth
from flask_jwt_extended import jwt_required
from api.v1.services.auth.logout import logout


@auth.route('/logout')
@swag_from('/api/v1/views/auth/documentation/logout.yml')
@jwt_required()
def user_logout():
    return logout()
