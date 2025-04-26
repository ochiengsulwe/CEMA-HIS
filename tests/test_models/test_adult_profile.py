import pytest
from models.adult_profile import AdultProfile
from models.child_profile import ChildProfile
from models.loginfo import LogInfo
from models.user import User
from tests.conftest import check_module_docstring


@pytest.fixture
def sample_loginfo(db_session):
    loginfo = LogInfo(account_type='adult', email='trial@test.com',
                      acc_status='verified')
    loginfo.password = 'validpassword'
    db_session.add(loginfo)
    db_session.flush()
    db_session.commit()
    return loginfo


@pytest.fixture
def sample_adult_profile(db_session, sample_loginfo):
    adult_profile = AdultProfile(
            phone_number='23456',
            permanent_location='Asego',
            current_location='Kanyada',
            loginfo_id=sample_loginfo.id
        )
    db_session.add(adult_profile)
    db_session.flush()
    db_session.commit()
    return adult_profile


def test_adult_profile_module_docstring():
    check_module_docstring(AdultProfile)


def test_create_adult_profile(db_session, sample_loginfo):
    adult = AdultProfile(
            phone_number='12345678',
            permanent_location='Lokichar',
            current_location='Lokichogio',
            loginfo_id=sample_loginfo.id
        )
    db_session.add(adult)
    db_session.flush()  # Ensures constraints are validated before commit
    db_session.commit()

    created_adult = AdultProfile.query.filter_by(id=adult.id).first()
    assert created_adult is not None
    assert created_adult.phone_number == '12345678'
    assert created_adult.permanent_location == 'Lokichar'
    assert created_adult.current_location == 'Lokichogio'
    assert created_adult.loginfo_id == sample_loginfo.id


def test_loginfo_relationship(db_session, sample_adult_profile):
    adult = sample_adult_profile
    assert adult.loginfo is not None
    assert adult.loginfo_id == adult.loginfo.id


def test_next_of_kin_relationship(db_session, sample_adult_profile):
    next_of_kin = AdultProfile(
            phone_number="5555555555",
            permanent_location="Nakuru",
            urrent_location="Thika",
            next_of_kin_id=sample_adult_profile.id
        )
    db_session.add(next_of_kin)
    db_session.commit()

    assert next_of_kin.next_of_kin is not None
    assert next_of_kin.next_of_kin.id == sample_adult_profile.id
    assert sample_adult_profile.dependents[0].id == next_of_kin.id


def test_children_relationship(db_session, sample_adult_profile):
    child_loginfo = LogInfo(
            account_type='child',
            acc_status='verified'
        )
    db_session.add(child_loginfo)
    db_session.commit()

    child = ChildProfile(
            loginfo_id=child_loginfo.id
        )
    sample_adult_profile.children.append(child)
    db_session.add(child)
    db_session.commit()

    assert len(sample_adult_profile.children) == 1
    assert sample_adult_profile.children[0].id == child.id
    assert child.parents[0].id == sample_adult_profile.id


def test_user_relationship(db_session, sample_adult_profile):
    identity = User(
            first_name='John',
            middle_name='Privy',
            last_name='Doe',
            gender='Male'
        )
    db_session.add(identity)

    sample_adult_profile.identity = identity

    db_session.commit()

    assert sample_adult_profile.identity_id == identity.id
    assert identity.adult == sample_adult_profile
