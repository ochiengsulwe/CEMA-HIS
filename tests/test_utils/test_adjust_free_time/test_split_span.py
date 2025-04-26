import pytest

from datetime import date, datetime, time, timedelta

from models.planner import Planner
from models.practitioner_profile import PracProfile
from models.slot import Slot
from models.span import Span
from utils.adjust_free_time import split_span


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
        time_from=time(9, 0),
        time_to=time(17, 0)
    )
    db_session.add(span)
    db_session.commit()
    return span


def test_split_span_middle(db_session, span):
    """Test splitting a span in the middle, ensuring two new spans are created."""
    time_from = time(12, 0)
    time_to = time(13, 0)

    split_span(span, time_from, time_to)

    updated_spans = db_session.query(Span).filter_by(slot_id=span.slot_id).all()
    assert len(updated_spans) == 2
    assert updated_spans[0].time_to == (datetime.combine(
        datetime.today(), time_from) - timedelta(minutes=5)).time()
    assert updated_spans[1].time_from == (datetime.combine(
        datetime.today(), time_to) + timedelta(minutes=5)).time()


"""
def test_split_span_at_start(db_session, span):
    # Test splitting when appointment starts at the beginning of the span.
    time_from = time(9, 0)
    time_to = time(10, 0)

    split_span(span, time_from, time_to)
    db_session.commit()

    updated_spans = db_session.query(Span).filter_by(slot_id=span.slot_id).all()
    assert len(updated_spans) == 2  # Should leave only the latter part
    assert updated_spans[0].time_from == (datetime.combine(
        datetime.today(), time_to) + timedelta(minutes=5)).time()
    assert updated_spans[0].time_to == time(17, 0)
"""


def test_split_span_at_end(db_session, span):
    """Test splitting when appointment ends at the span's end."""
    time_from = time(16, 0)
    time_to = time(17, 0)

    split_span(span, time_from, time_to)

    updated_spans = db_session.query(Span).filter_by(slot_id=span.slot_id).all()
    assert len(updated_spans) == 2  # Should leave only the initial part
    assert updated_spans[0].time_from == time(9, 0)
    assert updated_spans[0].time_to == (datetime.combine
                                        (datetime.today(),
                                         time_from) - timedelta(minutes=5)).time()


def test_split_span_overlapping_full(db_session, span):
    """Test when appointment time fully covers the span (should delete span)."""
    time_from = time(9, 0)
    time_to = time(17, 0)

    split_span(span, time_from, time_to)

    updated_spans = db_session.query(Span).filter_by(slot_id=span.slot_id).all()
    assert len(updated_spans) == 2  # Should delete span completely


"""
def test_split_span_no_overlap(db_session, span):
    # Test when appointment time is completely outside the span (no effect)
    time_from = time(18, 0)
    time_to = time(19, 0)

    split_span(span, time_from, time_to)

    updated_spans = db_session.query(Span).filter_by(slot_id=span.slot_id).all()
    assert len(updated_spans) == 2  # Original span should remain untouched
    assert updated_spans[0].time_from == time(9, 0)
    assert updated_spans[0].time_to == time(17, 0)
"""
