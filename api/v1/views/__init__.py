"""The dunder file registers error blueprints"""
from flask import Blueprint

errors = Blueprint('errors', __name__)

from api.v1.views import error
