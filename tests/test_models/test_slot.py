import pytest

from datetime import date, time
from sqlalchemy.exc import IntegrityError

from models.planner import Planner
from models.practitioner_profile import PracProfile
from models.slot import Slot
from models.span import Span

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

    db_session.add(planner)
    db_session.commit()

    return planner


@pytest.fixture
def slot(db_session, planner):
    slot = Slot(
        planner=planner,
        date=date(2020, 5, 1)
    )
    db_session.add(slot)
    db_session.commit()
    return slot


def test_appointment_module_docstring():
    check_module_docstring(Slot)


def test_slot_creation(db_session, planner):
    slot = Slot(planner=planner, date=date(2020, 5, 1))
    db_session.add(slot)

    assert slot.planner == planner
    assert slot.date is not None
    assert slot.id is not None
    assert slot.created_at is not None
    assert slot.updated_at is not None


@pytest.mark.parametrize("field", ["planner_id", "date"])
def test_slot_missing_required_fields(db_session, field, planner):
    """Test that missing required fields raises an IntegrityError."""
    kwargs = {
        "planner_id": planner.id,
        "date": date(2020, 5, 1)
    }

    del kwargs[field]  # Remove the field being tested

    slot = Slot(**kwargs)

    db_session.add(slot)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_slot_can_have_multiple_spans(db_session, slot):
    """Test that an appointment can be associated with multiple schedules."""

    span1 = Span(
        slot=slot,
        time_from=time(9, 20),
        time_to=time(9, 40)
    )
    span2 = Span(
        slot=slot,
        time_from=time(9, 20),
        time_to=time(9, 40)
    )

    db_session.add_all([span1, span2])
    db_session.commit()

    assert len(slot.spans) == 2
    assert span1 in slot.spans
    assert span2 in slot.spans


def test_deleting_slot_deletes_spans(db_session, slot):
    """Test that deleting an appointment deletes related schedules
        due to cascade delete."""

    span1 = Span(
        slot=slot,
        time_from=time(9, 20),
        time_to=time(9, 40)

    )
    span2 = Span(
        slot=slot,
        time_from=time(9, 20),
        time_to=time(9, 40)
    )

    db_session.add_all([span1, span2])
    db_session.commit()

    assert db_session.query(Span).count() == 2

    db_session.delete(slot)
    db_session.commit()

    # Schedules should be deleted due to cascade
    assert db_session.query(Span).count() == 0


def test_deleting_span_removes_span_from_slot_spans_list(db_session, slot):
    span1 = Span(
        slot=slot,
        time_from=time(9, 20),
        time_to=time(9, 40)
    )
    span2 = Span(
        slot=slot,
        time_from=time(9, 20),
        time_to=time(9, 40)
    )

    db_session.add_all([span1, span2])
    db_session.commit()

    assert db_session.query(Span).count() == 2
    assert len(slot.spans) == 2
    assert span1 in slot.spans
    assert span2 in slot.spans

    span1.delete()
    db_session.commit()
    assert len(slot.spans) == 1
    assert span2 in slot.spans
    assert db_session.query(Span).count() == 1

    span2.delete()
    db_session.commit()
    assert slot.spans == []
    assert db_session.query(Span).count() == 0
