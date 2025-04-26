"""
This endpoint allows a practitioner to create an account to this system
"""
from flask import request
from flasgger.utils import swag_from

from api.v1.views.auth import auth
from api.v1.services.auth.create_account.practitioner import create_practitioner_account


@auth.route('/create_account/practitioner', methods=['POST'])
@swag_from('/api/v1/views/auth/documentation/create_account/practitioner.yml')
def practitioner_create_account():
    data = request.get_json()
    return create_practitioner_account(data)
