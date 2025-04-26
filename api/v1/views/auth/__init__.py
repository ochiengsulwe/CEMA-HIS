"""The dunder file registers the blueprints auth"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

from api.v1.views.auth.create_account import (
        adult, dependant, practitioner
        )
from api.v1.views.auth.login import adult, practitioner
from api.v1.views.auth import logout
