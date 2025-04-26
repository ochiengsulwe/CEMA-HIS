# import pytest

from datetime import date, time

from models.planner import Planner
from models.practitioner_profile import PracProfile
from models.slot import Slot
from models.span import Span

from utils.overlap import span_find

"""
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
    planner = Planner(prac_profile_id=prac.id, practitioner=prac)

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
        time_from=time(9, 30),
        time_to=time(9, 50)
    )
    db_session.add(span)
    db_session.commit()
    return span
"""


def test_exact_match(db_session):
    """Test case where the requested time exactly matches an existing span."""
    prac = PracProfile(
        fee=2500,
        profession='Doctor',
        prof_reg_year=date(2020, 5, 1),
        profession_reg='PR-001'
    )
    db_session.add(prac)
    db_session.commit()
    planner = Planner(practioner=prac, prac_profile_id=prac.id)
    db_session.add(planner)
    db_session.commit()
    slot = Slot(
        planner=planner,
        date=date(2020, 5, 1)
    )
    db_session.add(slot)
    db_session.commit()
    span = Span(
        slot=slot,
        time_from=time(9, 30),
        time_to=time(9, 50)
    )
    db_session.add(span)
    db_session.commit()
    result = span_find(prac, date(2020, 5, 1), time(9, 30), time(9, 50))
    assert result is not None


def test_within_existing_span(db_session):
    """Test case where the requested time is fully inside an existing span."""
    prac = PracProfile(
        fee=2500,
        profession='Doctor',
        prof_reg_year=date(2020, 5, 1),
        profession_reg='PR-001'
    )
    db_session.add(prac)
    db_session.commit()
    planner = Planner(practitioner=prac, prac_profile_id=prac.id)
    db_session.add(planner)
    db_session.commit()
    slot = Slot(
        planner=planner,
        date=date(2020, 5, 1)
    )
    db_session.add(slot)
    db_session.commit()
    span = Span(
        slot=slot,
        time_from=time(9, 30),
        time_to=time(9, 50)
    )
    db_session.add(span)
    db_session.commit()
    result = span_find(prac, date(2020, 5, 1), time(9, 35), time(9, 40))
    assert result is not None


def test_no_overlap(db_session):
    """Test case where the requested time does not fit in any existing span."""
    prac = PracProfile(
        fee=2500,
        profession='Doctor',
        prof_reg_year=date(2020, 5, 1),
        profession_reg='PR-001'
    )
    db_session.add(prac)
    db_session.commit()
    planner = Planner(practitioner=prac, prac_profile_id=prac.id)
    db_session.add(planner)
    db_session.commit()
    slot = Slot(
        planner=planner,
        date=date(2020, 5, 1),
    )
    db_session.add(slot)
    db_session.commit()
    span = Span(
        slot=slot,
        time_from=time(9, 30),
        time_to=time(9, 50)
    )
    db_session.add(span)
    db_session.commit()
    result = span_find(prac, date(2020, 5, 1), time(10, 0), time(11, 0))
    assert result is None


def test_span_boundary_start(db_session):
    """Test case where requested time starts before an available span."""
    prac = PracProfile(
        fee=2500,
        profession='Doctor',
        prof_reg_year=date(2020, 5, 1),
        profession_reg='PR-001',
    )
    db_session.add(prac)
    db_session.commit()
    planner = Planner(practitioner=prac, prac_profile_id=prac.id)
    db_session.add(planner)
    db_session.commit()
    slot = Slot(
        planner=planner,
        date=date(2020, 5, 1)
    )
    db_session.add(slot)
    db_session.commit()
    span = Span(
        slot=slot,
        time_from=time(9, 30),
        time_to=time(9, 50)
    )
    db_session.add(span)
    db_session.commit()
    result = span_find(prac, date(2020, 5, 1), time(9, 0), time(9, 40))
    assert result is None


def test_span_boundary_end(db_session):
    """Test case where requested time ends after an available span."""
    prac = PracProfile(
        fee=2500,
        profession='Doctor',
        prof_reg_year=date(2020, 5, 1),
        profession_reg='PR-001'
    )
    db_session.add(prac)
    db_session.commit()
    planner = Planner(practitioner=prac, prac_profile_id=prac.id)
    db_session.add(planner)
    slot = Slot(
        planner=planner,
        date=date(2020, 5, 1)
    )
    db_session.add(slot)
    db_session.commit()
    span = Span(
        slot=slot,
        time_from=time(9, 30),
        time_to=time(9, 50)
    )
    db_session.add(span)
    db_session.commit()
    result = span_find(prac, date(2020, 5, 1), time(9, 40), time(10, 30))
    assert result is None


def test_different_date(db_session):
    """Test case where a span exists but on a different date."""
    prac = PracProfile(
        fee=2500,
        profession='Doctor',
        prof_reg_year=date(200, 5, 1),
        profession_reg='PR-001'
    )
    db_session.add(prac)
    db_session.commit()
    planner = Planner(practitioner=prac, prac_profile_id=prac.id)
    db_session.add(planner)
    db_session.commit()
    slot = Slot(
        planner=planner,
        date=date(2020, 5, 1)
    )
    db_session.add(slot)
    db_session.commit()
    span = Span(
        slot=slot,
        time_from=time(9, 30),
        time_to=time(9, 50)
    )
    db_session.add(span)
    db_session.commit()
    result = span_find(prac, date(2025, 5, 1), time(10, 0), time(11, 0))
    assert result is None
