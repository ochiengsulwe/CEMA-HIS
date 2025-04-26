import pytest

from models.user import User
from utils.database import record_integrity


def test_record_integrity_success(db_session):
    """Test successful record creation."""
    record = record_integrity(db_session, User, first_name='ochi', last_name='sulwe',
                              gender='Male', id_number=1111)
    db_session.commit()

    assert record is not None
    assert record.first_name == "ochi"
    assert record.last_name == "sulwe"
    assert record.gender == 'Male'
    assert record.id_number == 1111


@pytest.mark.parametrize("unique_field, value",
                         [
                             ("id_number", 111),
                             ("passport_number", "A123"),
                             ("birth_cert_number", 1000),
                         ])
def test_record_integrity_duplicate_entry(db_session, unique_field, value):
    """Test handling of duplicate unique constraint violations."""
    base_data = {
        "first_name": "sulwe",
        "last_name": "ochi",
        "gender": "Male"
    }

    # Appending unique fields to base data
    kwargs = {**base_data, unique_field: value}
    record_integrity(db_session, User, **kwargs)
    db_session.commit()

    with pytest.raises(ValueError,
                       match=f"The .*'{value}' provided exists"):
        record_integrity(db_session, User, **kwargs)
        db_session.commit()
