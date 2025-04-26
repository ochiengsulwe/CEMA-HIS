"""
This module defines how all appointments will be retrieved for adults only.

No filtering in this case, all of them are retrieved. A very expensive transaction.
"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.v1 import db
from models import storage
from models.loginfo import LogInfo
from utils.support import count_schedules


def appointments():
    """
        Retrieves all appointment information for the authenticated adult user.

        Returns:
            tuple: response containing a list of appointments or an error message, and
                associated HTTP repsonse code
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        user = storage.get(LogInfo, current_user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        if user.account_type == 'adult':
            appointments = user.adult_profile.appointments
        else:
            return jsonify({'error': 'not authorised'}), 403

        appointments = {}
        for app in appointments:
            if user.account_type == 'adult':
                name_ = app.practitioner.identity
            else:
                return jsonify({'error': 'not authorised'}), 403

            first_name = name_.first_name
            middle_name = name_.middle_name
            last_name = name_.last_name
            name = " ".join(filter(None, [first_name, middle_name, last_name]))

            upc = count_schedules(app, 'pending')
            comp = count_schedules(app, 'complete')
            all = upc + comp
            appointments.update({
                "appointment_id": app.id,
                "appointment_status": app.status,
                "appointment_type": app.type,
                "appointment_with": name,
                "all_visits": all,
                "upcoming_visits": upc,
                "complete_visits": comp
            })

        return jsonify(appointments), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
