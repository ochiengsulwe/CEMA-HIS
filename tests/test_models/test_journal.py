import pytest
from models.journal import Journal
from models.adult_profile import AdultProfile
from models.child_profile import ChildProfile
from models.loginfo import LogInfo


@pytest.fixture
def sample_loginfo(db_session):
    loginfo = LogInfo(account_type='adult', email='trial@test.com',
                      acc_status='verified')
    loginfo.password = 'validpassword'
    db_session.add(loginfo)
    db_session.flush()
    db_session.commit()
    yield loginfo


@pytest.fixture
def sample_adult_profile(db_session, sample_loginfo):
    """Fixture to create a sample AdultProfile."""
    adult = AdultProfile(
        phone_number="1234567890",
        permanent_location="Nairobi",
        current_location="Mombasa",
        loginfo=sample_loginfo
    )
    db_session.add(adult)
    db_session.flush()
    yield adult


@pytest.fixture
def sample_child_profile(db_session, sample_adult_profile):
    """Fixture to create a sample ChildProfile."""
    child = ChildProfile(
        created_by=sample_adult_profile.loginfo
    )
    child.parents.append(sample_adult_profile)
    db_session.add(child)
    db_session.flush()
    yield child


def test_create_adult_journal(db_session, sample_adult_profile):
    """Test creating a Journal and verifying its attributes."""
    journal = Journal(
        body="This is a test adult journal entry.",
        adult_id=sample_adult_profile.id
    )
    db_session.add(journal)
    db_session.flush()  # Ensures constraints are validated before commit
    db_session.commit()

    created_journal = Journal.query.filter_by(id=journal.id).first()
    assert created_journal is not None
    assert created_journal.body == "This is a test adult journal entry."
    assert created_journal.adult_id == sample_adult_profile.id


def test_journaled_by_relationship(db_session, sample_adult_profile,
                                   sample_child_profile):
    """Test the journaled_by relationship of the Journal model."""
    journal = Journal(
        body="Child journal created by this adult.",
        child_id=sample_child_profile.id,
        journaled_by_id=sample_adult_profile.id
    )
    db_session.add(journal)
    db_session.flush()
    db_session.commit()

    assert journal.journaled_by == sample_adult_profile
    assert journal in sample_adult_profile.journals_created
    assert sample_child_profile in sample_adult_profile.children
