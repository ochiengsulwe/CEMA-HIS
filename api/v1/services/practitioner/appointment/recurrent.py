"""The module describes marking an appointment as recurrent

    This actually means changing an appointment status to recurrent
"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.appointment import Appointment
from models.loginfo import LogInfo


def repeat_appointment(appointment_id):
    """
    Change appointment from default `once` to `recurrent`

    This should only be possible after the pratitioner has had an appointment with the
        patient. Meaning updated_at attribute should never be greater than schedule's
        time_from attribute(but might be => time_to).

    Args:
        appointment_id (str): the unique appointment identifier

    Returns:
        tuple: A success or error message, coupled with the respective HTTPS response
            code.
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'error': 'not authorised'}), 401

    try:
        user_ = storage.get(LogInfo, current_user_id)

        if not user_:
            return jsonify({'error': 'user not found'}), 404

        if user_.account_type == 'practitioner':
            user = user_.prac_profile
        else:
            return jsonify({'error': 'not authorised'}), 403

        appointment = storage.get(Appointment, appointment_id)
        if not appointment:
            return jsonify({'error': 'appointment details not found'}), 404

        if appointment not in user.appointments:
            return jsonify({'error': 'not authorised'}), 403

        appointment.type = 'repeat'
        appointment.save()
        return jsonify({'message': 'appointment updated successfuly'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
