import pytest
from datetime import date

from models.loginfo import LogInfo
from models.practitioner_profile import PracProfile
from models.user import User

from tests.conftest import check_module_docstring


@pytest.fixture
def sample_loginfo(db_session):
    loginfo = LogInfo(
            account_type='practitioner',
            email='trial@test.com',
            acc_status='verified')
    loginfo.password = 'validpassword'
    db_session.add(loginfo)
    db_session.flush()
    db_session.commit()

    return loginfo


@pytest.fixture
def sample_prac_profile(db_session, sample_loginfo):
    practitioner = PracProfile(
            bio='Experienced medical practitioner',
            profession_reg='PR-001',
            prof_reg_year=date(2020, 5, 1),
            profession='Doctor',
            fee=2500,
            specialization='Pediatrics',
            specialization_reg='SPR-123',
            spec_reg_year=date(2021, 7, 1),
            loginfo_id=sample_loginfo.id
        )
    db_session.add(practitioner)
    db_session.flush()
    db_session.commit()

    return practitioner


def test_prac_profile_module_docstring():
    check_module_docstring(PracProfile)


def test_create_prac_profile(db_session, sample_loginfo):
    loginfo = sample_loginfo

    prac_profile = PracProfile(
        bio='Experienced medical practitioner',
        profession_reg='PR-001',
        prof_reg_year=date(2020, 5, 1),
        profession='Doctor',
        fee=2500,
        specialization='Pediatrics',
        specialization_reg='SPR-123',
        spec_reg_year=date(2021, 7, 1),
        loginfo_id=loginfo.id
    )
    db_session.add(prac_profile)
    db_session.commit()

    assert prac_profile.id is not None
    assert prac_profile.profession == 'Doctor'
    assert prac_profile.loginfo == loginfo
    assert prac_profile.loginfo_id == loginfo.id
    assert prac_profile.bio is not None
    assert prac_profile.profession_reg == 'PR-001'
    assert prac_profile.specialization == 'Pediatrics'
    assert prac_profile.prof_reg_year is not None
    assert prac_profile.spec_reg_year is not None
    assert prac_profile.fee is not None


def test_loginfo_relationship(db_session, sample_prac_profile):
    practitioner = sample_prac_profile
    assert practitioner.loginfo is not None
    assert practitioner.loginfo_id == practitioner.loginfo.id


def test_user_relationship(db_session, sample_prac_profile):
    identity = User(
            first_name='John',
            middle_name='Privy',
            last_name='Doe',
            gender='Male'
        )
    db_session.add(identity)
    sample_prac_profile.identity = identity
    db_session.commit()

    assert sample_prac_profile.identity_id == identity.id
    assert identity.practitioner == sample_prac_profile
