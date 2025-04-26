"""
This view allows an Adult user to create an account for their dependant
"""
from flask import request
from flask_jwt_extended import jwt_required
from flasgger.utils import swag_from

from api.v1.services.auth.create_account.dependant import create_account_child
from api.v1.views.auth import auth


@auth.route('/create_account/child', methods=['POST'])
@swag_from('/api/v1/views/auth/documentation/create_account/child.yml')
@jwt_required()
def create_child_account():
    data = request.get_json()
    return create_account_child(data)
