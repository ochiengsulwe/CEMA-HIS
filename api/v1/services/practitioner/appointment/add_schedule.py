from datetime import datetime
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db

from models import storage
from models.appointment import Appointment
from models.loginfo import LogInfo
from models.schedule import Schedule

from utils.adjust_free_time import adjust_planner
from utils.create_planner import create_planner
from utils.database import record_integrity
from utils.general import data_check
from utils.overlap import schedule_overlap, span_find, date_find


def add_appointment_schedule(data, appointment_id):
    """
    Books an appointment with a practitioner for an adult user

    Args:
        data (dict): a dictionary containing appointment schedule information
        appointment_id (str): appointment unique identifier

    Returns:
        tuple: A repsonse message and an associated HTTP code
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'error': 'not authorised'}), 403

    required_fields = ['date', 'time_from', 'time_to']
    if not data:
        return jsonify({'error': 'not json'}), 400

    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    time_from = datetime.strptime(data['time_from'], '%H:%M').time()
    time_to = datetime.strptime(data['time_to'], '%H:%M').time()
    s_status = 'pending'

    error_response = data_check(data, required_fields)
    if error_response:
        return error_response

    appointment = storage.get(Appointment, appointment_id)
    if not appointment:
        return jsonify({'error': 'appointment information not found'}), 404

    if appointment.type == 'once':
        return jsonify({'error': 'not allowed'}), 401

    prac_profile = storage.get(LogInfo, current_user_id)
    if not prac_profile:
        return jsonify({'error': 'practitioner not found'}), 404
    prac = prac_profile.prac_profile
    if not prac:
        return jsonify({'error': 'practitioner not found'}), 404

    # finding the span to allocate the new appointment time
    if not date_find(prac, date):
        create_planner(db.session, prac.id, date, time_from, time_to)

    free = span_find(prac, date, time_from, time_to)
    if not free:
        return jsonify({'error': 'booked at this time'}), 404
    try:
        # No overlapping appointments for the user if user has other appointments.
        if appointment.adult_profile:
            user = appointment.adult_profile
        elif appointment.child_profile:
            user = appointment.child_profile
        else:
            return jsonify({'error': 'no user profile found'}), 404

        if user.appointments:
            overlapping_appointment = schedule_overlap(user, date, time_from, time_to)
            if overlapping_appointment:
                return jsonify(
                        {
                            'error': 'already have another appointment at this time. '
                            'Please choose another time.'
                        }
                 ), 409

        schedule = record_integrity(db.session, Schedule,
                                    time_from=time_from,
                                    time_to=time_to,
                                    date=date,
                                    status=s_status,
                                    appointment=appointment
                                    )
        appointment.save()
        schedule.save()
        appointment.schedules.append(schedule)

        # yunking appointment time from prac's span above(free)
        adjust_planner(free, time_from, time_to)
        storage.save()

        return jsonify({'message': 'appointment schedule successfully added'}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
