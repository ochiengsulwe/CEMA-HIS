from flask import jsonify

from api.v1 import db

from models import storage
from models.loginfo import LogInfo
from models.user import User
from models.practitioner_profile import PracProfile
from models.proxy.practitioners.clinical_officer import ClinicalOfficer
from models.proxy.practitioners.dentist import Dentist
from models.proxy.practitioners.dietitian import Dietitian
from models.proxy.practitioners.doctor import Doctor
from models.proxy.practitioners.lab_tech import LabTech
from models.proxy.practitioners.nurse import Nurse
from models.proxy.practitioners.pharmacist import Pharmacist
from models.proxy.practitioners.physiotherapist import Physiotherapist
from models.proxy.practitioners.psychologist import Psychologist

from utils.database import check_email_exists, record_integrity
from utils.general import data_check


def create_practitioner_account(data):
    """
    This method creates a Practitioner System Account (Profile)

    Practitoners can be of various professions within the healthcare sector.
    This method checks against a (hypothetical) Union Databases to check if the
        practitoner registering in this system is registered to a Union before allowing
        for a registration only if the practitoner is registered with a Union.

    Args:
        data (dict): a dictionary containing the necessary information for account
            creation.
    Raises:
        ValueError: when a wrong value is provided in the attributes
    Returns:
        tuple: a message on success or an error on failure, coupled with crorresponding
            HTTP code
    """
    required_fields = [
                'email', 'fee', 'password', 'profession_type',
                'profession_reg', 'phone_number'
    ]
    practitioners = {
        "ClinicalOfficer": ClinicalOfficer, "Dentist": Dentist,
        "Dietitian": Dietitian, "Doctor": Doctor, "LabTech": LabTech,
        "Nurse": Nurse, "Pharmacist": Pharmacist,
        "Physiotherapist": Physiotherapist, "Psychologist": Psychologist
    }

    if not data:
        return jsonify({'message': 'not json'}), 400

    email = data.get('email')
    password = data.get('password')
    profession_type = data.get('profession_type')
    fee = data.get('fee')
    account_type = 'practitioner'
    profession_reg = data.get('profession_reg')
    phone_number = data.get('phone_number')
    acc_status = 'verified'

    if check_email_exists(db.session, LogInfo, email, account_type):
        return jsonify(
            {
                'error': (
                    f"The email {email} already in use for account type {account_type}"
                )
            }
        ), 409

    error_response = data_check(data, required_fields)
    if error_response:
        return error_response

    profession = practitioners.get(profession_type)
    if not profession:
        return jsonify(
                {'error': f"The profession type {profession_type} is not valid"}
                ), 400

    """
    Querying third party database to check if registering practitioner is
    registered with their associated Board.
    """
    practitioner = db.session.query(profession).filter(
            profession.license_num == profession_reg).first()
    if practitioner is None:
        message = "Please register with your professional body first.Thank you"
        return jsonify({'message': message}), 400

    """Check if practitioner exists in our own database"""
    exists = db.session.query(User).filter(
            User.id_number == practitioner.id_num).first()
    if not exists:
        error_response = data_check(data, required_fields)
        if error_response:
            return error_response

        try:
            new_user = record_integrity(db.session, User,
                                        first_name=practitioner.first_name,
                                        middle_name=practitioner.middle_name,
                                        last_name=practitioner.last_name,
                                        gender=practitioner.gender,
                                        id_number=practitioner.id_num)

            login_details = record_integrity(db.session, LogInfo,
                                             email=email,
                                             account_type=account_type,
                                             acc_status=acc_status,
                                             password=password)
            profile = record_integrity(db.session, PracProfile,
                                       loginfo_id=login_details.id,
                                       profession_reg=practitioner.license_num,
                                       phone_number=phone_number,
                                       identity_id=new_user.id,
                                       fee=fee,
                                       profession=profession_type,
                                       prof_reg_year=practitioner.reg_year)
            if practitioner.spec_reg_num is not None:
                profile.specialization_reg = practitioner.spec_reg_num
                profile.specialization = practitioner.specialization
                profile.spec_reg_year = practitioner.spec_year

            storage.new(profile)
            storage.save()

            response_data = new_user.to_dict()
            mess = f'account for ({new_user.first_name}) was created successfully'
            response_data['message'] = mess
            return jsonify(response_data), 201

        except ValueError as e:
            return jsonify({'error': str(e)}), 409
    # If user is present, just append new login details.
    else:
        # Check if there is a LogInfo entry with account_type 'practitioner'
        if check_email_exists(db.session, LogInfo, email, account_type):
            return jsonify(
                    {
                        'error': (
                                  f"The email {email} already in use"
                                  f" for account type {account_type}"
                                )
                    },
                ), 409
        if exists.practitioner is not None:
            response = f'practioner account for ID {exists.id_number} exists'
            return jsonify({'message': response}), 409

        error_response = data_check(data, required_fields)
        if error_response:
            return error_response

        try:
            login_details = record_integrity(db.session, LogInfo,
                                             email=email,
                                             account_type=account_type,
                                             acc_status=acc_status,
                                             password=password)
            profile = record_integrity(db.session, PracProfile,
                                       loginfo_id=login_details.id,
                                       profession_reg=practitioner.license_num,
                                       profession=profession_type,
                                       identity_id=exists.id,
                                       phone_number=phone_number,
                                       prof_reg_year=practitioner.reg_year)
            if practitioner.spec_reg_num is not None:
                profile.specialization_reg = practitioner.spec_reg_num
                profile.specialization = practitioner.specialization
                profile.spec_reg_year = practitioner.spec_year

            storage.new(profile)
            storage.save()
            response_data = exists.to_dict()
            mess = f'account for ({exists.first_name}) was created successfully'
            response_data['message'] = mess

            return jsonify(response_data), 201

        except ValueError as e:
            return jsonify({'error': str(e)}), 409
