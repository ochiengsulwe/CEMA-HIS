from datetime import datetime
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.appointment import Appointment
from models.child_profile import ChildProfile
from models.h_prog import HealthProgram
from models.loginfo import LogInfo
from models.practitioner_profile import PracProfile
from models.prac_program import PractitionerProgram
from models.schedule import Schedule

from utils.adjust_free_time import adjust_planner
from utils.database import record_integrity
from utils.general import data_check
from utils.overlap import schedule_overlap, span_find
from utils.support import is_parent


def child_book_appointment(data, child_id, prac_id, program_id):
    """
    Books an appointment with a practitioner for a child user

    Args:
        data (dict): a dictionary containing appointment information
        child_id (str): child's profile unique ID
        prac_id (str): the practitioner offering the program
        program_id (str): the program the adult wants to sign up the child

    Returns:
        tuple: A response message and an associated HTTP code
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'error': 'not authorised'}), 403

    required_fields = ['date', 'time_from', 'time_to']
    if not data:
        return jsonify({'error': 'not json'}), 400

    error_response = data_check(data, required_fields)
    if error_response:
        return error_response

    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    time_from = datetime.strptime(data['time_from'], '%H:%M').time()
    time_to = datetime.strptime(data['time_to'], '%H:%M').time()
    status = 'confirmed'
    s_status = 'pending'
    appointment_type = 'once'

    parent_info = storage.get(LogInfo, current_user_id)
    if not parent_info:
        return jsonify({'error': 'patient information not found'}), 404

    child = storage.get(ChildProfile, child_id)
    if not child:
        return jsonify({'error': 'child information not found'}), 404

    if not is_parent(child, parent_info):
        return jsonify({'error': 'not authorised'}), 403

    prac_profile = storage.get(PracProfile, prac_id)
    if not prac_profile:
        return jsonify({'error': 'practitioner not found'}), 404

    program = storage.get(HealthProgram, program_id)
    if not program:
        return jsonify({'error': 'appointment not found'}), 404

    prac_program = db.session.query(PractitionerProgram).filter_by(
        practitioner=prac_profile, program=program).first()
    if not prac_program:
        return jsonify({'error': 'practitioner is not linked to this program'}), 404

    free = span_find(prac_profile, date, time_from, time_to)
    if not free:
        mes = f"{prac_profile.identity.last_name} is booked at this time!"
        return jsonify({'error': mes}), 409

    try:
        if child.appointments:
            overlapping_appointment = schedule_overlap(child, date, time_from, time_to)
            if overlapping_appointment:
                return jsonify({
                    'error': 'child already has another appointment at this time. '
                             'Please choose another time.'
                }), 409

            for app in child.appointments:
                if (
                    app.practitioner_id == prac_id and
                        app.program_id == program_id
                ):
                    mes = (f"child already have an appointment with "
                           f"{prac_profile.identity.first_name} "
                           f"{prac_profile.identity.last_name} for this program.")
                    return jsonify({'error': mes}), 409

        appointment = record_integrity(db.session, Appointment,
                                       child_profile=child,
                                       practitioner=prac_profile,
                                       type=appointment_type,
                                       status=status,
                                       program_id=program_id)

        schedule = record_integrity(db.session, Schedule,
                                    time_from=time_from,
                                    time_to=time_to,
                                    date=date,
                                    status=s_status,
                                    appointment=appointment)

        appointment.save()
        schedule.save()
        appointment.schedules.append(schedule)

        if child not in prac_program.enrolled_children:
            prac_program.enrolled_children.append(child)

        adjust_planner(free, time_from, time_to)
        storage.save()

        return jsonify({'message': 'appointment booked successfully'}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
