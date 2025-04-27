from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from api.v1.services.patient.appointment.child.book import child_book_appointment

# Blueprint
from api.v1.views.patient import patient


@patient.route('/child/<child_id>/<program_id>/<prac_id>/appointment/book',
               methods=['POST'])
@swag_from('/api/v1/views/patient/documentation/appointment/child/book.yml')
@jwt_required()
def book_child_appointment(program_id, prac_id, child_id):
    data = request.get_json()
    return child_book_appointment(data, child_id, prac_id, program_id)
