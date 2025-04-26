# import pytest

from datetime import date, time

from models.appointment import Appointment
from models.practitioner_profile import PracProfile
from models.schedule import Schedule

from utils.overlap import schedule_overlap

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
def appointment(db_session, prac):
    appointment = Appointment(
        practitioner=prac,
        practitioner_id=prac.id,
        status='confirmed',
        type='once'
    )

    db_session.add(appointment)
    db_session.commit()

    db_session.refresh(prac)

    return appointment


@pytest.fixture
def schedule(db_session, appointment):
    schedule = Schedule(
        appointment_id=appointment.id,
        appointment=appointment,
        time_from=time(9, 30),
        time_to=time(9, 50),
        date=date(2020, 5, 1),
        status='complete'
    )
    db_session.add(schedule)
    db_session.commit()

    return schedule
"""


def test_no_overlap(db_session):
    """Test case where no overlapping appointment exists."""
    prac = PracProfile(
        fee=2500,
        profession_reg='PR-001',
        prof_reg_year=date(2020, 5, 1),
        profession='Doctor'
    )
    db_session.add(prac)
    db_session.commit()
    appointment = Appointment(
        practitioner=prac,
        status='confirmed',
        type='once'

    )
    db_session.add(appointment)
    db_session.commit()
    schedule = Schedule(
        appointment=appointment,
        time_from=time(9, 30),
        time_to=time(9, 50),
        date=date(2020, 5, 1),
        status='complete'
    )
    db_session.add(schedule)
    db_session.commit()
    db_session.refresh(prac)
    assert len(prac.appointments) == 1
    date_ = prac.appointments[0].schedules[0].date
    assert date_ == date(2020, 5, 1)
    result = schedule_overlap(prac, date(2020, 5, 1), time(10, 15), time(10, 20))
    assert result is None


def test_exact_match_overlap(db_session):
    """Test case where the new appointment exactly matches an existing one."""
    prac = PracProfile(
        fee=2500,
        profession='Doctor',
        prof_reg_year=date(2020, 5, 1),
        profession_reg='PR-001'
    )
    db_session.add(prac)
    db_session.commit()
    appointment = Appointment(
        practitioner=prac,
        status='confirmed',
        type='once'
    )
    db_session.add(appointment)
    db_session.commit()
    schedule = Schedule(
        appointment=appointment,
        status='complete',
        date=date(2020, 5, 1),
        time_from=time(9, 30),
        time_to=time(9, 50)
    )
    db_session.add(schedule)
    db_session.commit()

    result = schedule_overlap(prac, date(2020, 5, 1), time(9, 30), time(9, 50))
    assert result is not None


def test_partial_overlap_start(db_session):
    """Test case where the new appointment starts inside an existing one."""
    prac = PracProfile(
        fee=2500,
        profession='Doctor',
        profession_reg='PR-001',
        prof_reg_year=date(2020, 5, 1)
    )
    db_session.add(prac)
    db_session.commit()
    appointment = Appointment(
        practitioner=prac,
        status='confirmed',
        type='once'
    )
    db_session.add(appointment)
    db_session.commit()
    schedule = Schedule(
        appointment=appointment,
        status='complete',
        date=date(2020, 5, 1),
        time_from=time(9, 30),
        time_to=time(9, 50)
    )
    db_session.add(schedule)
    db_session.commit()
    result = schedule_overlap(prac, date(2020, 5, 1), time(9, 40), time(10, 30))
    assert result is not None


def test_partial_overlap_end(db_session):
    """Test case where the new appointment ends inside an existing one."""
    prac = PracProfile(
        fee=2500,
        profession='Doctor',
        prof_reg_year=date(2020, 5, 1),
        profession_reg='PR-001'
    )
    db_session.add(prac)
    db_session.commit()
    appointment = Appointment(
        practitioner=prac,
        status='confirmed',
        type='once'
    )
    db_session.add(appointment)
    db_session.commit()
    schedule = Schedule(
        appointment=appointment,
        status='complete',
        date=date(2020, 5, 1),
        time_from=time(9, 30),
        time_to=time(9, 50)
    )
    db_session.add(schedule)
    db_session.commit()
    result = schedule_overlap(prac, date(2020, 5, 1), time(9, 35), time(9, 40))
    assert result is not None


def test_no_overlap_different_date(db_session):
    """Test case where the date is different, so no overlap should be found."""

    prac = PracProfile(
        fee=2500,
        profession='Doctor',
        prof_reg_year=date(2020, 5, 1),
        profession_reg='PR-001',
    )
    db_session.add(prac)
    db_session.commit()
    appointment = Appointment(
        practitioner=prac,
        type='once',
        status='confirmed',
    )
    db_session.add(appointment)
    db_session.commit()
    schedule = Schedule(
        appointment=appointment,
        status='complete',
        date=date(2020, 5, 1),
        time_from=time(9, 30),
        time_to=time(9, 50)
    )
    db_session.add(schedule)
    db_session.commit()
    result = schedule_overlap(prac, date(2025, 5, 2), time(10, 0), time(11, 0))
    assert result is None
