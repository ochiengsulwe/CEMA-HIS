import pytest
from datetime import datetime

from api.v1 import db
from models.engine.db_storage import DBStorage
from models.user import User
from models.child_profile import ChildProfile


@pytest.fixture
def db_storage():
    """Fixture for DBStorage instance."""
    return DBStorage()


@pytest.fixture
def sample_user():
    """Fixture for creating a sample User instance."""
    return User(
        first_name="John",
        last_name="Doe",
        gender="Male",
        date_of_birth=datetime(1990, 5, 12)
    )


@pytest.fixture
def sample_child_profile(sample_user):
    """Fixture for creating a sample ChildProfile instance."""
    return ChildProfile(
        user=sample_user,
        date_of_birth=datetime(2020, 6, 15)
    )


def test_new_and_save(db_session, db_storage, sample_user):
    """Test that objects can be added and saved to the database."""
    db_storage.new(sample_user)
    db_storage.save()

    saved_user = db.session.query(User).filter_by(id=sample_user.id).first()
    assert saved_user is not None
    assert saved_user.first_name == "John"
    assert saved_user.last_name == "Doe"


def test_all_model_classes(db_session, db_storage, sample_child_profile, sample_user):
    """Test that all returns correct data."""
    db_storage.new(sample_user)
    db_storage.new(sample_child_profile)
    db_storage.save()

    # Get all objects
    all_objects = db_storage.all()
    assert len(all_objects) == 2
    assert any(isinstance(obj, User) for obj in all_objects.values())
    assert any(isinstance(obj, ChildProfile) for obj in all_objects.values())


def test_one_model_class(db_session, db_storage, sample_user):
    # Get only User objects
    db_storage.new(sample_user)
    db_storage.save()

    user_objects = db_storage.all(User)
    assert len(user_objects) == 1
    assert isinstance(list(user_objects.values())[0], User)


def test_delete(db_storage, sample_user):
    """Test that objects can be deleted from the database."""
    db_storage.new(sample_user)
    db_storage.save()

    # Verify the user was saved
    saved_user = db.session.query(User).filter_by(first_name="John").first()
    assert saved_user is not None

    # Delete the user
    db_storage.delete(sample_user)
    db_storage.save()

    # Verify the user was deleted
    deleted_user = db.session.query(User).filter_by(first_name="John").first()
    assert deleted_user is None


def test_get(db_session, db_storage, sample_user):
    """Test that get retrieves the correct object."""
    db_storage.new(sample_user)
    db_storage.save()

    # Retrieve the user
    retrieved_user = db_storage.get(User, sample_user.id)
    assert retrieved_user is not None
    assert retrieved_user.first_name == "John"
    assert retrieved_user.id == sample_user.id


def test_count(db_session, db_storage, sample_user, sample_child_profile):
    """Test that count returns the correct number of objects."""
    db_storage.new(sample_user)
    db_storage.new(sample_child_profile)
    db_storage.save()

    # Count all objects
    total_count = db_storage.count()
    assert total_count == 2

    # Count User objects
    user_count = db_storage.count(User)
    assert user_count == 1

    # Count ChildProfile objects
    child_count = db_storage.count(ChildProfile)
    assert child_count == 1


def test_close(db_storage):
    """Test that close removes the session."""
    db_storage.close()
    assert db.session.registry.has() is False


def test_all_no_class(db_session, db_storage, sample_user, sample_child_profile):
    """Test all without specifying a class."""
    db_storage.new(sample_user)
    db_storage.new(sample_child_profile)
    db_storage.save()

    all_objects = db_storage.all()
    assert len(all_objects) == 2


def test_get_invalid_class(db_storage):
    """Test get method raises ValueError for an invalid class name."""
    with pytest.raises(ValueError):
        db_storage.get("InvalidClass", "some_id")
