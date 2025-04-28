from flask import jsonify

from flask_jwt_extended import create_access_token
from models.loginfo import LogInfo
from api.v1 import db
from utils.general import data_check


def login_adult(data):
    """
    This service allows a valid user (who is not a practitioner) to log into the system

    Args:
        data (dict): a bundled information needed for account access confirmation
    Returns:
        tuple: a message, JTW_TOKEN on success or an error, coupled with a matching
            HTTP code

    """
    required_fields = ['email', 'password']

    if not data:
        return jsonify({'message': 'not json'}), 400
    data_check(data, required_fields)

    password = data.get('password')
    email = data.get('email')
    account_type = 'adult'

    user = db.session.query(LogInfo).filter_by(email=email,
                                               account_type=account_type
                                               ).first()
    if user is not None and user.verify_password(password):
        access_token = create_access_token(identity=user.id)
        mes = 'Sucessfully Logged In'
        return jsonify(
            {'message': mes, 'account_type': user.account_type,
             'access_token': access_token}), 200
    return jsonify({'message': 'invalid email or password.'}), 401
