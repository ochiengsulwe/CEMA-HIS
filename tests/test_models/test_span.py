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
    check_module_docstring(Span)


def test_span_creation(db_session, slot):
    span = Span(
        slot=slot,
        time_from=time(9, 30),
        time_to=time(9, 50)
    )
    db_session.add(span)

    assert span.slot == slot
    assert span.time_from is not None
    assert span.time_to is not None
    assert slot.id is not None
    assert span.id is not None
    assert span.created_at is not None
    assert span.updated_at is not None


@pytest.mark.parametrize("field", ["slot_id", "time_from", "time_to"])
def test_span_missing_required_fields(db_session, field, slot):
    """Test that missing required fields raises an IntegrityError."""
    kwargs = {
        "slot_id": slot.id,
        "time_from": time(9, 30),
        "time_to": time(9, 50)
    }

    del kwargs[field]  # Remove the field being tested

    span = Span(**kwargs)

    db_session.add(span)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_deleting_planner_deletes_slot_and_spans(db_session, slot):
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

    assert db_session.query(Planner).count() == 1
    assert db_session.query(Slot).count() == 1
    assert db_session.query(Span).count() == 2

    db_session.delete(slot.planner)
    db_session.commit()

    # Slots and spans should be deleted due to cascade
    assert db_session.query(Planner).count() == 0
    assert db_session.query(Planner).count() == 0
    assert db_session.query(Planner).count() == 0


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
