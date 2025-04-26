import pytest

from datetime import date, datetime, time, timedelta

from models.planner import Planner
from models.practitioner_profile import PracProfile
from models.slot import Slot
from models.span import Span
from utils.adjust_free_time import adjust_planner, split_span


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


def test_adjust_planner_deletes_exact_match(db_session, slot):
    span = Span(slot=slot, time_from=time(10, 0), time_to=time(12, 0))
    db_session.add(span)
    db_session.commit()

    adjust_planner(span, time(10, 0), time(12, 0))
    assert db_session.query(Span).filter_by(id=span.id).first() is None


def test_adjust_planner_updates_time_from(db_session, slot):
    span = Span(slot=slot, time_from=time(10, 0), time_to=time(12, 0))
    db_session.add(span)
    db_session.commit()

    adjust_planner(span, time(10, 0), time(11, 0))
    updated_span = db_session.query(Span).filter_by(id=span.id).first()
    assert updated_span.time_from == (datetime.combine(
        datetime.today(), time(11, 0)) + timedelta(minutes=5)).time()


def test_adjust_planner_updates_time_to(db_session, slot):
    span = Span(slot=slot, time_from=time(10, 0), time_to=time(12, 0))
    db_session.add(span)
    db_session.commit()

    adjust_planner(span, time(11, 0), time(12, 0))
    updated_span = db_session.query(Span).filter_by(id=span.id).first()
    assert updated_span.time_to == (datetime.combine(
        datetime.today(), time(11, 0)) - timedelta(minutes=5)).time()


def test_adjust_planner_splits_span(db_session, slot):
    span = Span(slot=slot, time_from=time(10, 0), time_to=time(20, 0))
    db_session.add(span)
    db_session.commit()

    adjust_planner(span, time(12, 0), time(14, 0))
    assert db_session.query(Span).filter_by(id=span.id).first() is None
    new_spans = db_session.query(Span).filter_by(slot_id=slot.id).all()
    assert len(new_spans) == 2


def test_split_span_creates_two_spans(db_session, slot):
    span = Span(slot=slot, time_from=time(10, 0), time_to=time(20, 0))
    db_session.add(span)
    db_session.commit()

    split_span(span, time(12, 0), time(14, 0))
    assert db_session.query(Span).filter_by(id=span.id).first() is None
    new_spans = db_session.query(Span).filter_by(slot_id=slot.id).all()
    assert len(new_spans) == 2

    assert new_spans[0].time_to == (datetime.combine(
        datetime.today(), time(12, 0)) - timedelta(minutes=5)).time()
    assert new_spans[1].time_from == (datetime.combine(
        datetime.today(), time(14, 0)) + timedelta(minutes=5)).time()
