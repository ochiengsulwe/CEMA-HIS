from flask import jsonify

from api.v1 import db

from models import storage
from models.adult_profile import AdultProfile
from models.loginfo import LogInfo
from models.proxy.users.adult import Citizen
from models.user import User

from utils.database import check_email_exists, record_integrity
from utils.general import data_check


def create_adult_account(data):
    """
    This method creates an Adult System Account (Profile)

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
                'email', 'password', 'phone_number', 'id_number'
    ]

    if not data:
        return jsonify({'message': 'not json'}), 400

    email = data.get('email')
    password = data.get('password')
    account_type = 'adult'
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
    id_num = int(data.get('id_number'))
    user = db.session.query(User).filter(User.id_number == id_num).first()

    if not user:
        error_response = data_check(data, required_fields)
        if error_response:
            return error_response
        adult = db.session.query(Citizen).filter(
                                 Citizen.id_num == id_num).first()
        if adult:
            try:
                new_user = record_integrity(db.session, User,
                                            first_name=adult.first_name,
                                            middle_name=adult.middle_name,
                                            gender=adult.gender,
                                            date_of_birth=adult.date_of_birth,
                                            last_name=adult.last_name,
                                            id_number=adult.id_num)

                login_details = record_integrity(db.session, LogInfo,
                                                 account_type=account_type,
                                                 email=email,
                                                 acc_status=acc_status,
                                                 password=password)
                profile = record_integrity(db.session, AdultProfile,
                                           loginfo_id=login_details.id,
                                           identity_id=new_user.id,
                                           permanent_location=adult.home_sub_location,
                                           phone_number=phone_number)

                storage.new(profile)
                storage.save()
                response_data = new_user.to_dict()
                response_data['message'] = (
                        f'account for ({new_user.first_name}) was created successfully'
                        )
                return jsonify(response_data), 201

            except ValueError as e:
                return jsonify({'error': str(e)}), 409

        else:
            message = f"ID Number: {id_num} doesn't exist."
            return jsonify({'message': message}), 404
    else:
        if check_email_exists(db.session, LogInfo, email, account_type):
            return jsonify(
                    {
                        'error': (
                                  f"The email {email} already in use"
                                  f" for account type {account_type}"
                            )
                    }
                ), 409

        if user.adult is not None:
            response = f'account for ID {user.id_number} exists'
            return jsonify({'message': response}), 409

        eu_fields = ['email', 'password', 'phone_number']
        error_response = data_check(data, eu_fields)
        if error_response:
            return error_response
        adult = db.session.query(Citizen).filter(
                                 Citizen.id_num == id_num).first()
        try:
            login_details = record_integrity(db.session, LogInfo,
                                             email=email,
                                             account_type=account_type,
                                             acc_status=acc_status,
                                             password=password)
            profile = record_integrity(db.session, AdultProfile,
                                       loginfo_id=login_details.id,
                                       identity_id=user.id,
                                       phone_number=phone_number,
                                       permanent_location=adult.home_sub_location)

            storage.new(profile)
            storage.save()
            response_data = user.to_dict()
            response_data['message'] = (
                    f'account for ({user.first_name}) was created successfully'
                    )
            return jsonify(response_data), 201

        except ValueError as e:
            return jsonify({'error': str(e)}), 409
