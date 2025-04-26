from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import IntegrityError
from api.v1 import db
from models import storage
from models.diagnostics.order import TestOrder
from models.schedule import Schedule
from models.loginfo import LogInfo
from utils.database import record_integrity


def create_test_order(schedule_id):
    """
    Create a new TestOrder for the given schedule_id.

    Args:
        schedule_id (str): ID of the current schedule.

    Returns:
        tuple: JSON response and HTTP status code
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'not signed in'}), 401

        prac = storage.get(LogInfo, current_user_id)
        if not prac or prac.account_type != 'practitioner':
            return jsonify({'error': 'not authorised'}), 403

        practitioner = prac.prac_profile
        if not practitioner:
            return jsonify({'error': 'practitioner not found'}), 404

        schedule = storage.get(Schedule, schedule_id)
        if not schedule:
            return jsonify({'error': 'schedule not found'}), 404

        appt = schedule.appointment
        if appt not in practitioner.appointments:
            return jsonify({'error': 'not authorised'}), 403

        test_order = record_integrity(db.session, TestOrder,
                                      schedule=schedule,
                                      status='ordered'
                                      )
        test_order.save()

        return jsonify({'message': 'TestOrder created successfully'}), 201

    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Database error occurred.", "details": str(e)}, 500
    except Exception as e:
        db.session.rollback()
        return {"error": "Unexpected error occurred.", "details": str(e)}, 500
