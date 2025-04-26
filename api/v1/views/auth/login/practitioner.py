"""
This view allows for a practitioner user to log into the system
"""
from flask import request
from flasgger.utils import swag_from

from api.v1.views.auth import auth
from api.v1.services.auth.login.practitioner import login_practitioner


@auth.route('/login/practitioner', methods=['POST'])
@swag_from('/api/v1/views/auth/documentation/login/practitioner_login.yml')
def practitioner_login():
    data = request.get_json()
    return login_practitioner(data)
