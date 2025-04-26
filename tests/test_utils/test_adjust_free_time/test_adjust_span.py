import pytest

from datetime import date, datetime, time, timedelta

from models.planner import Planner
from models.practitioner_profile import PracProfile
from models.slot import Slot
from models.span import Span
from utils.adjust_free_time import adjust_span


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


@pytest.fixture
def span(db_session, slot):
    span = Span(
        slot=slot,
        time_from=time(10, 0),
        time_to=time(20, 15)
    )
    db_session.add(span)
    db_session.commit()
    return span


def test_adjust_span_updates_time_from(span):
    """Test that span.time_from is updated to time_to + 5 minutes."""
    time_to = time(10, 30)

    adjust_span(span, time_to)

    expected_time = (datetime.combine(
        datetime.today(), time_to) + timedelta(minutes=5)).time()
    assert span.time_from == expected_time


"""
def test_adjust_span_near_midnight(slot):
    Test edge case when time_to is close to midnight.
    span = Span(
        time_from=time(23, 50),
        time_to=time(0, 0),
        slot=slot
    )
    time_to = time(23, 59)  # Appointment ends at 23:59

    adjust_span(span, time_to)

    expected_time = (datetime.combine(
        datetime.today(), time_to) + timedelta(minutes=5)).time()
    assert span.time_from == expected_time


def test_adjust_span_exact_midnight(slot):
    Test edge case when time_to is exactly 00:00.
    span = Span(
        time_from=time(23, 45),
        time_to=time(0, 0),
        slot=slot
    )
    time_to = time(0, 0)  # Appointment ends at 00:00

    adjust_span(span, time_to)

    expected_time = (datetime.combine(
        datetime.today(), time_to) + timedelta(minutes=5)).time()
    assert span.time_from == expected_time

"""


@pytest.mark.parametrize("invalid_time_to", ["12:30", 12345, None, object(), (9, 90),
                                             (13, 500)])
def test_adjust_span_invalid_time_to(invalid_time_to, span):
    """Test that passing invalid time_to raises an error."""

    with pytest.raises((TypeError, ValueError)):
        adjust_span(span, invalid_time_to)


def test_adjust_span_none_values(span):
    """Test that passing None values raises an error."""
    with pytest.raises(TypeError):
        adjust_span(span, None)


def test_adjust_span_invalid_span():
    """Test that passing an invalid span object raises an error."""
    with pytest.raises(AttributeError):
        adjust_span(None, time(10, 0))
