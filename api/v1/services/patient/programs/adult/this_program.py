from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from models import storage
from models.loginfo import LogInfo


def retrieve_enrolled_program(program_id):
    """
    Retrieves details of a specific enrolled health program for an adult patient.

    Args:
        program_id (str): ID of the enrolled program.

    Returns:
        tuple: response containing program details or an error message, and
               associated HTTP response code
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        if not user.adult_profile:
            return jsonify({'error': 'user profile not found'}), 404

        enrolled_program = next(
            (p for p in user.adult_profile.enrolled_programs if p.id == program_id),
            None
        )

        if not enrolled_program:
            return jsonify({'error': 'program not found'}), 404

        program = enrolled_program.program

        practitioner = (enrolled_program.practitioner.identity
                        if enrolled_program.practitioner else None)
        practitioner_name = (f"{practitioner.first_name} {practitioner.last_name}"
                             if practitioner else None)

        appointments = [
            app for app in user.adult_profile.appointments
            if app.program_id == program.id
        ]

        schedule_dates = []
        for appointment in appointments:
            for schedule in appointment.schedules:
                schedule_dates.append(schedule.date)

        if schedule_dates:
            start_date = min(schedule_dates).isoformat()
            end_date = max(schedule_dates).isoformat()
        else:
            start_date = end_date = None

        program_info = {
            "program_id": program.id,
            "offered_by": practitioner_name,
            "start_date": start_date,
            "end_date": end_date,
            "description": program.description
        }

        return jsonify(program_info), 200

    except SQLAlchemyError as e:
        return jsonify({'error': 'database error', 'details': str(e)}), 500
