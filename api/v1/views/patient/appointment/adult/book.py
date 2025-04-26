from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.adult.book import adult_book_appointment

# Blueprint
from api.v1.views.patient import patient


@patient.route('/appointment/book', methods=['POST'])
@swag_from('/api/v1/views/patient/documentation/appointment/adult/book.yml')
@jwt_required()
def book_adult_appointment():
    data = request.get_json()
    return adult_book_appointment(data)
