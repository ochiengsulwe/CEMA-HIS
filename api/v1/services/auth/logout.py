from flask import jsonify
from flask_jwt_extended import get_jwt
from api.v1 import db
from models.token_blocklist import TokenBlocklist


def logout():
    """
    Invalidate JWT by adding it to the blocklist.
    Returns:
        tuple: a message of success
    """
    jwt = get_jwt()
    jti = jwt["jti"]  # JWT unique identifier

    # Add token to the blocklist
    new_entry = TokenBlocklist(jti=jti)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'message': 'Successfully logged out'}), 200
