from api.v1.views import errors
from flask import jsonify


@errors.app_errorhandler(400)
def bad_request(error):
    response = {
        'error': 'Bad Request',
        'message': str(error)
    }
    return jsonify(response), 400


@errors.app_errorhandler(401)
def unauthorized(error):
    response = {
        'error': 'Unauthorized',
        'message': str(error)
    }
    return jsonify(response), 401


@errors.app_errorhandler(403)
def forbidden(error):
    response = {
        'error': 'Forbidden',
        'message': str(error)
    }
    return jsonify(response), 403


@errors.app_errorhandler(404)
def not_found(error):
    response = {
        'error': 'Not Found',
        'message': 'The requested resource could not be found'
    }
    return jsonify(response), 404


@errors.app_errorhandler(409)
def conflict(error):
    response = {
        'error': 'Conflict',
        'message': str(error)
    }
    return jsonify(response), 409


@errors.app_errorhandler(500)
def internal_server_error(error):
    response = {
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }
    return jsonify(response), 500
