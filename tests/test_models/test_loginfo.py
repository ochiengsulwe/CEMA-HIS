import pytest
from sqlalchemy.exc import DataError, IntegrityError, StatementError

from models.loginfo import LogInfo
from models.adult_profile import AdultProfile
# from models.practitioner_profile import PracProfile
from tests.conftest import check_module_docstring


def test_loginfo_module_docstring():
    check_module_docstring(LogInfo)


def test_loginfo_creation(db_session):
    """Test if LogInfo can be created and fields are set properly."""
    log_info = LogInfo(
        account_type='practitioner',
        email='practitioner@example.com',
        acc_status='active'
    )
    db_session.add(log_info)
    db_session.commit()

    assert log_info.id is not None
    assert log_info.account_type == 'practitioner'
    assert log_info.email == 'practitioner@example.com'
    assert log_info.acc_status == 'active'
    assert log_info.created_at is not None
    assert log_info.updated_at is not None


def test_loginfo_password_handling(db_session):
    """Test password property and verification functionality."""
    log_info = LogInfo(
        account_type='admin',
        email='admin@example.com',
        acc_status='active'
    )
    log_info.password = 'SecurePassword123'

    db_session.add(log_info)
    db_session.commit()

    # Check password hash is set and password verification
    assert log_info.password_hash is not None
    assert log_info.verify_password('SecurePassword123') is True
    assert log_info.verify_password('WrongPassword') is False

    # Ensure password is not readable
    with pytest.raises(AttributeError):
        _ = log_info.password


def test_loginfo_relationships(db_session):
    """Test if LogInfo relationships with other models work properly."""
    log_info = LogInfo(
        account_type='adult',
        email='adultuser@example.com',
        acc_status='verified'
    )
    adult_profile = AdultProfile(
        phone_number='1234567890',
        permanent_location='Nairobi',
        loginfo=log_info
    )
    db_session.add(log_info)
    db_session.add(adult_profile)
    db_session.commit()

    assert adult_profile.loginfo == log_info
    assert log_info.adult_profile == adult_profile


@pytest.mark.parametrize("account_type, acc_status",
                         [
                             ("invalid_type", "verified"),
                             ("adult", "not_a_status"),
                             ("wrong_value", "unknown"),
                         ]
                         )
def test_loginfo_enum_constraints(db_session, account_type, acc_status):
    """Test if invalid enum values are rejected."""
    log_info = LogInfo(
        account_type=account_type,
        email='invalid@example.com',
        acc_status=acc_status
    )
    with pytest.raises((DataError, IntegrityError, StatementError)):
        db_session.add(log_info)
        db_session.commit()
