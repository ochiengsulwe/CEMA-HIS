"""
This route exposes the Adult User to create their individual User account.
"""
from flasgger.utils import swag_from
from flask import request

from api.v1.views.auth import auth
from api.v1.services.auth.create_account.adult import create_adult_account


@auth.route('/create_account/adult', methods=['POST'])
@swag_from('/api/v1/views/auth/documentation/create_account/adult.yml')
def adult_create_account():
    data = request.get_json()
    return create_adult_account(data)
