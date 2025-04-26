import pytest

from models.adult_profile import AdultProfile
from models.child_profile import ChildProfile
from models.loginfo import LogInfo
from models.user import User
from tests.conftest import check_module_docstring


@pytest.fixture
def sample_loginfo(db_session):
    loginfo = LogInfo(
            account_type='child',
            acc_status='verified')
    db_session.add(loginfo)
    db_session.flush()
    db_session.commit()
    return loginfo


@pytest.fixture
def sample_child_profile(db_session, sample_loginfo):
    loginfo = sample_loginfo
    child_profile = ChildProfile(
            loginfo_id=loginfo.id
            )
    db_session.add(child_profile)
    db_session.flush()
    db_session.commit()
    return child_profile


@pytest.fixture
def sample_adult_profile(db_session):
    loginfo = LogInfo(
            account_type='adult',
            email='trial@test.com',
            acc_status='verified'
        )
    loginfo.password = 'validpassword'
    db_session.add(loginfo)

    adult = AdultProfile(
            phone_number='23456',
            permanent_location='Asego',
            current_location='Kanyada',
            loginfo_id=loginfo.id
        )
    db_session.add(adult)
    db_session.flush()
    db_session.commit()

    return adult


def test_child_profile_module_docstring():
    check_module_docstring(ChildProfile)


def test_create_child_profile(db_session, sample_loginfo):
    child = ChildProfile(
            loginfo_id=sample_loginfo.id
        )
    db_session.add(child)
    db_session.flush()
    db_session.commit()

    created_child = ChildProfile.query.filter_by(id=child.id).first()
    assert created_child is not None
    assert created_child.loginfo_id == sample_loginfo.id


def test_loginfo_relationship(db_session, sample_child_profile):
    child = sample_child_profile
    assert child.loginfo is not None
    assert child.loginfo_id == child.loginfo.id


def test_parents_relationship(db_session, sample_child_profile,
                              sample_adult_profile):
    adult = sample_adult_profile
    child = sample_child_profile

    child.parents.append(adult)
    db_session.flush()
    db_session.commit()

    assert len(child.parents) == 1
    assert child.parents[0].id == adult.id
    assert adult.children[0].id == child.id


def test_created_by_parent_relationship(db_session, sample_loginfo,
                                        sample_adult_profile):
    adult = sample_adult_profile

    child = ChildProfile(
            loginfo_id=sample_loginfo.id,
            created_by_id=adult.loginfo.id
        )
    db_session.add(child)
    db_session.flush()
    db_session.commit()

    assert child.created_by is not None
    assert child.created_by_id == adult.loginfo.id


def test_user_relationship(db_session, sample_child_profile):
    identity = User(
            first_name='John',
            middle_name='Privy',
            last_name='Doe',
            gender='Male'
        )

    db_session.add(identity)

    sample_child_profile.identity = identity

    db_session.commit()
    assert sample_child_profile.identity_id == identity.id
    assert identity.child == sample_child_profile
