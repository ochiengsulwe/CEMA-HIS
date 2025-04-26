"""
This view allows for an adult user to log into the system
"""
from flask import request
from flasgger.utils import swag_from
from api.v1.services.auth.login.adult import login_adult
from api.v1.views.auth import auth


@auth.route('/login/adult', methods=['POST'])
@swag_from('/api/v1/views/auth/documentation/login/adult_login.yml')
def adult_login():
    data = request.get_json()
    return login_adult(data)
