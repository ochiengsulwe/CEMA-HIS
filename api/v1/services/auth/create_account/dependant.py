from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from api.v1 import db

from models import storage
from models.child_profile import ChildProfile
from models.loginfo import LogInfo
from models.proxy.users.child import Child
from models.user import User

from utils.database import record_integrity
from utils.general import data_check


def create_account_child(data):
    """
    This method creates a Child System Account (Profile)

    This can only be done by a parent/guardian of the child

    Args:
        data (dict): a dictionary containing the necessary information for account
            creation.
    Raises:
        ValueError: when a wrong value is provided in the attributes
    Returns:
        tuple: a message on success or an error on failure, coupled with crorresponding
            HTTP code
    """
    required_fields = ['birth_cert_number']
    if not data:
        return jsonify({'message': 'not json'}), 400
    current_user_id = get_jwt_identity()

    if not current_user_id:
        return jsonify({'mesasge': 'not signed in'}), 401

    parent_info = storage.get(LogInfo, current_user_id)
    if not parent_info:
        return jsonify({'mesasge': 'user not found'}), 404

    account_type = 'child'
    acc_status = 'verified'
    error_response = data_check(data, required_fields)
    if error_response:
        return error_response
    birth_num = int(data.get('birth_cert_number'))

    child = db.session.query(User).filter(User.birth_cert_number == birth_num).first()

    if not child:
        error_response = data_check(data, required_fields)
        if error_response:
            return error_response
        registered = db.session.query(Child).filter(
                                      Child.birth_cert_number == birth_num).first()
        if registered:
            try:
                new_born = record_integrity(db.session, User,
                                            first_name=registered.first_name,
                                            middle_name=registered.middle_name,
                                            last_name=registered.last_name,
                                            gender=registered.gender,
                                            date_of_birth=registered.date_of_birth,
                                            birth_cert_number=(
                                                registered.birth_cert_number))
                login_details = record_integrity(db.session, LogInfo,
                                                 account_type=account_type,
                                                 account_status=acc_status)
                profile = record_integrity(db.session, ChildProfile,
                                           loginfo_id=login_details.id,
                                           identity=new_born,
                                           created_by=parent_info)

                if parent_info.account_type != 'practitioner':
                    profile.parents.append(parent_info.adult_profile)
                parent_info.adult_profile.children.append(profile)

                storage.new(profile)
                storage.save()
                response_data = new_born.to_dict()
                response_data['message'] = (
                        f'account for ({new_born.first_name}) was created successfully'
                        )
                return jsonify(response_data), 201
            except ValueError as e:
                return jsonify({'error': str(e)}), 409
        else:
            message = f"Birth Certicate Number {birth_num} doesn't exists"
            return jsonify({'message': message}), 404

    return jsonify({"message": f"{child.first_name} has an existing account"}), 409
