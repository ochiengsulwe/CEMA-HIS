"""The module describes appointment completion.

    This actually means changing a schedule status to complete.
"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from models.schedule import Schedule


def complete_appointment(schedule_id):
    """
    Marks schedule as complete

    This should only be possible after the pratitioner has had an appointment with the
        patient. Meaning updated_at attribute should never be greater than schedule's
        time_from attribute(but might be => time_to).

    Args:
        schedule_id (str): the exact appointment schedule to update.

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

        schedule = storage.get(Schedule, schedule_id)
        if not schedule:
            return jsonify({'error': 'schedule not found'}), 404

        if schedule.appointment not in user.appointments:
            return jsonify({'error': 'not authorised'}), 403

        schedule.status = 'complete'
        schedule.save()
        return jsonify({'message': 'appointment completed'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
