import pytest
# import uuid
from datetime import date, datetime
# from unittest.mock import MagicMock

from models.adult_profile import AdultProfile
from models.base_model import BaseModel
from models.loginfo import LogInfo
from models.practitioner_profile import PracProfile
from models.user import User

from tests.conftest import check_module_docstring


@pytest.fixture
def base_model_instance():
    """Fixture for creating an instance of BaseModel."""
    return BaseModel()


@pytest.fixture
def loginfo_instance(db_session):
    loginfo = LogInfo(
            account_type='practitioner',
            email='practitioner@example.com',
            acc_status='active'
        )
    loginfo.password = 'SecurePassword123'
    db_session.add(loginfo)
    db_session.commit()

    return loginfo


@pytest.fixture
def practitioner_instance(db_session, loginfo_instance):
    practitioner = PracProfile(
            bio='Experienced medical practitioner',
            profession_reg='PR-001',
            prof_reg_year=date(2020, 5, 1),
            profession='Doctor',
            specialization='Pediatrics',
            specialization_reg='SPR-123',
            spec_reg_year=date(2021, 7, 1),
            loginfo_id=loginfo_instance.id
        )
    db_session.add(practitioner)
    db_session.commit()

    return practitioner


@pytest.fixture
def user_instance(db_session):
    user = User(
            first_name="Jane",
            middle_name="Doe",
            last_name="Smith",
            gender="Female",
            date_of_birth=date(1990, 1, 1),
            birth_cert_number=123456,
            id_number=98765432,
            passport_number="A1234567"
        )
    db_session.add(user)
    db_session.commit()

    return user


@pytest.fixture
def sample_adult_profile(db_session):
    loginfo = LogInfo(
            account_type='adult',
            email='adult@example.com',
            acc_status='active'
        )
    loginfo.password = 'SecurePassword123'
    db_session.add(loginfo)
    db_session.commit()

    adult_profile = AdultProfile(
            phone_number='23456',
            permanent_location='Asego',
            current_location='Kanyada',
            loginfo_id=loginfo.id
        )
    db_session.add(adult_profile)
    db_session.commit()

    return adult_profile


@pytest.fixture
def mock_inspect(mocker):
    mock_inspect = mocker.patch('sqlalchemy.inspection.inspect')
    mock_inspect.return_value.mapper.column_attrs = []
    return mock_inspect


@pytest.fixture
def mock_storage(mocker):
    return mocker.patch('models.storage', autospec=True)


def test_base_model_module_docstring():
    check_module_docstring(BaseModel)


def test_base_model_initialization(base_model_instance):
    """Test initialization of BaseModel."""
    assert isinstance(base_model_instance.id, str)
    assert len(base_model_instance.id) == 36  # UUID length
    assert isinstance(base_model_instance.created_at, datetime)
    assert isinstance(base_model_instance.updated_at, datetime)
    assert base_model_instance.created_at == base_model_instance.updated_at


def test_base_model_string_representation(base_model_instance):
    """Test string representation of BaseModel."""
    expected_str = (f"[BaseModel] ({base_model_instance.id}) "
                    f"{base_model_instance.__dict__}")
    assert str(base_model_instance) == expected_str


def test_base_model_save(mocker, base_model_instance):
    """Test the save method of BaseModel."""
    # Mock the models.storage to prevent actual database calls
    mock_storage = mocker.patch('models.storage')

    old_updated_at = base_model_instance.updated_at
    base_model_instance.save()

    # Check that updated_at has changed
    assert base_model_instance.updated_at > old_updated_at

    # Check that storage's new and save methods were called
    mock_storage.new.assert_called_once_with(base_model_instance)
    mock_storage.save.assert_called_once()


def test_base_model_to_dict(user_instance):
    result = user_instance.to_dict()

    assert isinstance(result, dict)
    assert result["id"] == user_instance.id
    assert result["created_at"] == user_instance.created_at.strftime(
        "%Y-%m-%dT%H:%M:%S")
    assert result["updated_at"] == user_instance.updated_at.strftime(
        "%Y-%m-%dT%H:%M:%S")
    assert result["__class__"] == "User"


def test_to_dict_excludes_sensitive_data(loginfo_instance):
    # sample_dict = loginfo_instance.to_dict()

    assert not hasattr(loginfo_instance, "password")

    sample_with_sensitive = loginfo_instance.to_dict(save_fs=True)
    assert "password_hash" in sample_with_sensitive


def test_base_model_to_dict_exclude_none(user_instance):
    user_instance.middle_name = None
    user_dict = user_instance.to_dict(exclude_none=True)
    assert "middle_name" not in user_dict

    user_dict_include_none = user_instance.to_dict(exclude_none=False)
    assert "middle_name" in user_dict_include_none
    assert user_dict_include_none["middle_name"] is None


def test_to_dict_excludes_empty_lists(user_instance):
    user_dict = user_instance.to_dict(exclude_none=True)
    assert "practitioner" not in user_dict
    user_dict = user_instance.to_dict(exclude_none=False)
    # assert "practitioner" in user_dict


def test_base_model_to_dict_include_relationships(mocker, base_model_instance):
    """Test that to_dict can include relationships."""
    mock_inspect = mocker.patch('models.base_model.inspect')
    mock_inspect().mapper.relationships = []

    result = base_model_instance.to_dict(include_relationships=True)
    assert isinstance(result, dict)


def test_base_model_delete(mocker, base_model_instance):
    """Test the delete method of BaseModel."""
    # Mock the models.storage to prevent actual database calls
    mock_storage = mocker.patch('models.storage')

    base_model_instance.delete()

    # Check that storage's delete method was called
    mock_storage.delete.assert_called_once_with(base_model_instance)


@pytest.mark.parametrize("kwargs", [
    {"created_at": "2024-11-18T12:50:00"},
    {"updated_at": "2024-11-18T12:50:00"},
    {"id": None}
])
def test_base_model_initialization_with_kwargs(kwargs):
    """Test BaseModel initialization with keyword arguments."""
    instance = BaseModel(**kwargs)
    if "created_at" in kwargs and isinstance(kwargs["created_at"], str):
        assert instance.created_at == datetime.strptime(kwargs["created_at"],
                                                        "%Y-%m-%dT%H:%M:%S")
    if "updated_at" in kwargs and isinstance(kwargs["updated_at"], str):
        assert instance.updated_at == datetime.strptime(kwargs["updated_at"],
                                                        "%Y-%m-%dT%H:%M:%S")
    if kwargs.get("id") is None:
        assert isinstance(instance.id, str)
