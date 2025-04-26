import pytest

from datetime import date, time

from models.date import Date
from models.planner import Planner
from models.practitioner_profile import PracProfile
from models.slot import Slot
from models.span import Span
from utils.create_planner import create_planner


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


"""
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
"""


def test_create_planner_success(db_session, prac, planner):
    """Tests if planner componenets are successfully created"""
    date_ = date.today()
    time_from = time(10, 0)
    time_to = time(20, 15)

    date_entry = Date(date=date_)
    db_session.add(date_entry)
    db_session.commit()

    response = create_planner(db_session, prac.id, date_, time_from, time_to)

    assert response is None
    assert db_session.query(Span).count() == 1
    assert db_session.query(Slot).count() == 1

    slot = db_session.query(Slot).first()
    span = db_session.query(Span).first()

    assert slot.planner == planner
    assert span.slot == slot
    assert slot.date == date_
    assert span.time_from == time_from
    assert span.time_to == time_to


def test_create_planner_prac_not_found(db_session, planner):
    """Tests for instances when an invalid practitoner tries to create aplanner"""
    date_ = date.today()
    time_from = time(10, 0)
    time_to = time(20, 15)
    prac = planner.id

    date_entry = Date(date=date_)
    db_session.add(date_entry)
    db_session.commit()

    response, status_code = create_planner(db_session, prac, date_, time_from, time_to)

    assert status_code == 404
    assert response.get_json() == {'error': 'practitioner not found'}


def test_create_planner_invalid_date(db_session, prac, planner):
    """
    Tests if invalid date is entered by the practitioner

    Invalid dates are those dates not captured in our databases:
        i. Dates before the initial date captured in the database, or
        ii. Date after the last date captured in the database
    """
    date_ = date.today()
    time_from = time(9, 0)
    time_to = time(20, 15)

    response, status_code = create_planner(db_session, prac.id, date_,
                                           time_from, time_to)

    assert response.get_json() == {"error": "invalid date"}
    assert status_code == 404


def test_create_planner_invalid_time_range(db_session, prac, planner):
    """
    Tests if time ranges are valid

    A valid time range is when time_from is always before time_to:
        i. valid range ==> time_from: (0, 0), time_to: (23:59) and anything in between
        ii. invalid range ==> time_from: (23, 59), time_to: (0, 0) and anything between
    """
    date_ = date.today()
    time_from = time(10, 0)
    time_to = time(9, 0)

    date_entry = Date(date=date_)
    db_session.add(date_entry)
    db_session.commit()

    response, status_code = create_planner(db_session, prac.id, date_,
                                           time_from, time_to)

    assert response.get_json() == {"error": "time_to must be greater than time_from"}
    assert status_code == 400


def test_create_planner_invalid_planner(db_session, prac):
    """
    Tests for invalid planner

    A planner is invalid if it doesn't exist in the database
    The absense of a planner may be due to:
        i. The entire deletion of the planner by matching practioner
        ii. If the planner has not just been created yet
    """
    date_ = date.today()
    time_from = time(9, 0)
    time_to = time(20, 15)

    prac = PracProfile(
        fee=2500,
        profession_reg='PR-002',
        prof_reg_year=date(2020, 5, 1),
        profession='Doctor'
    )
    date_entry = Date(date=date_)
    db_session.add_all([date_entry, prac])
    db_session.commit()

    response, status_code = create_planner(db_session, prac.id, date_,
                                           time_from, time_to)

    assert response.get_json() == {'error': 'practitioner planner not found'}
    assert status_code == 404
