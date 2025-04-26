import pytest

from datetime import date
from sqlalchemy.exc import IntegrityError

from models.planner import Planner
from models.practitioner_profile import PracProfile
from models.slot import Slot

from tests.conftest import check_module_docstring


@pytest.fixture
def prac(db_session):
    p = PracProfile(
        fee=2500,
        profession_reg='PR-001',
        prof_reg_year=date(2020, 5, 1),
        profession='Doctor'
    )
    db_session.add(p)
    db_session.commit()
    return p


@pytest.fixture
def planner(db_session, prac):
    planner = Planner(practitioner=prac)
    slot = Slot(
        planner=planner,
        date=date(2020, 5, 1)
    )

    db_session.add(planner)
    db_session.add(slot)
    db_session.commit()

    return planner


def test_appointment_module_docstring():
    check_module_docstring(Planner)


def test_planner_creation(db_session, prac):
    planner = Planner(practitioner=prac)
    db_session.add(planner)

    assert planner.practitioner == prac
    assert planner.id is not None
    assert planner.created_at is not None
    assert planner.updated_at is not None


def test_practitioner_not_null(db_session):
    planner = Planner()

    db_session.add(planner)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


@pytest.mark.parametrize("field", ["practitioner_id"])
def test_planner_missing_required_fields(db_session, field, prac):
    """Test that missing required fields raises an IntegrityError."""
    kwargs = {
        "practitioner_id": prac.id
    }

    del kwargs[field]  # Remove the field being tested

    planner = Planner(**kwargs)

    db_session.add(planner)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_planner_can_have_multiple_slots(db_session, planner):
    """Test that an appointment can be associated with multiple schedules."""

    slot1 = Slot(
        planner=planner,
        date=date(2020, 5, 1)
    )
    slot2 = Slot(
        planner=planner,
        date=date(2020, 5, 2)
    )

    db_session.add_all([slot1, slot2])
    db_session.commit()

    assert len(planner.slots) == 3
    assert slot1 in planner.slots
    assert slot2 in planner.slots


def test_deleting_planner_deletes_slots(db_session, planner):
    """
    Test that deleting a planner deletes related slots
        due to cascade delete.

    """
    slot1 = Slot(
        planner=planner,
        date=date(2020, 5, 1)
    )
    slot2 = Slot(
        planner=planner,
        date=date(2020, 5, 2)
    )

    db_session.add_all([slot1, slot2])
    db_session.commit()

    assert db_session.query(Slot).count() == 3

    db_session.delete(planner)
    db_session.commit()

    # Schedules should be deleted due to cascade
    assert db_session.query(Slot).count() == 0
