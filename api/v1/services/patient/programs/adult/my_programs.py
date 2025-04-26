from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from models import storage
from models.loginfo import LogInfo


def list_enrolled_programs():
    """
    Lists all health programs an adult patient is enrolled in,
        grouped by program name, and including practitioner info, start date,
        end date, and description.

    Returns:
        tuple: response containing grouped program details or an error message, and
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

        grouped_programs = defaultdict(list)

        for practitioner_program in user.adult_profile.enrolled_programs:
            program = practitioner_program.program
            practitioner = (practitioner_program.practitioner.identity
                            if practitioner_program.practitioner else None)
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
                "offered_by": practitioner_name,
                "start_date": start_date,
                "end_date": end_date,
                "description": program.description,
                "program_id": program.id
            }

            grouped_programs[program.name].append(program_info)

        return jsonify(grouped_programs), 200

    except SQLAlchemyError as e:
        return jsonify({'error': 'database error', 'details': str(e)}), 500
