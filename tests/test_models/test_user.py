import pytest

from models.user import User
from datetime import date

from tests.conftest import check_module_docstring


@pytest.fixture
def user_instance():
    """Fixture to create a valid User instance."""
    return User(
        first_name="Jane",
        middle_name="Doe",
        last_name="Smith",
        gender="Female",
        date_of_birth=date(1990, 1, 1),
        birth_cert_number=123456,
        id_number=98765432,
        passport_number="A1234567"
    )


def test_user_module_docstring():
    check_module_docstring(User)


def test_user_creation(db_session, user_instance):
    """Test that a User can be created and saved to the database."""
    db_session.add(user_instance)
    db_session.commit()

    retrieved_user = User.query.filter_by(id=user_instance.id).first()
    assert retrieved_user is not None
    assert retrieved_user.first_name == "Jane"
    assert retrieved_user.middle_name == "Doe"
    assert retrieved_user.last_name == "Smith"


def test_field_not_null(db_session, user_instance):
    """Test field constraints like non-nullable and unique."""
    # Test non-nullable constraints
    user_instance.first_name = None
    db_session.add(user_instance)
    with pytest.raises(Exception):
        db_session.commit()


def test_field_unique(db_session, user_instance):
    # Test unique constraints
    user_instance.first_name = "Jane"
    db_session.add(user_instance)
    db_session.commit()

    duplicate_user = User(
        first_name="John",
        last_name="Smith",
        gender="Male",
        birth_cert_number=123456  # Duplicate birth_cert_number
    )
    db_session.add(duplicate_user)
    with pytest.raises(Exception):
        db_session.commit()


def test_child_relationship(db_session, user_instance):
    """Test child relationship defined on the User model."""
    from models.child_profile import ChildProfile
    child = ChildProfile(
            identity=user_instance)
    db_session.add(child)
    db_session.commit()

    assert user_instance.child == child


def test_adult_relationship(db_session, user_instance):
    """Test adult relationship"""
    from models.adult_profile import AdultProfile
    adult = AdultProfile(
            phone_number='12345',
            permanent_location='Rakweba',
            current_location='Rikni',
            identity=user_instance
        )
    db_session.add(adult)
    db_session.commit()

    assert user_instance.adult == adult


def test_practitioner_relationship(db_session, user_instance):
    from models.practitioner_profile import PracProfile
    practitioner = PracProfile(
            bio='Some random text',
            profession_reg='1234',
            fee=2500,
            prof_reg_year=date(2019, 12, 29),
            profession='Doctor',
            identity=user_instance
        )
    db_session.add(practitioner)
    db_session.commit()

    assert user_instance.practitioner == practitioner


def test_user_update(db_session, user_instance):
    """Test updating a User instance."""
    db_session.add(user_instance)
    db_session.commit()

    user_instance.first_name = "Alice"
    db_session.commit()

    updated_user = User.query.filter_by(id=user_instance.id).first()
    assert updated_user.first_name == "Alice"


def test_user_deletion(db_session, user_instance):
    """Test deleting a User instance."""
    db_session.add(user_instance)
    db_session.commit()

    db_session.delete(user_instance)
    db_session.commit()

    deleted_user = User.query.filter_by(id=user_instance.id).first()
    assert deleted_user is None


def test_user_invalid_data(db_session):
    """Test invalid scenarios for User model."""
    invalid_user = User(
        first_name="John",
        last_name=None,  # Missing required field
        gender="Other",  # Invalid enum value
    )
    db_session.add(invalid_user)
    with pytest.raises(Exception):
        db_session.commit()
