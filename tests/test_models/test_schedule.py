import pytest

from datetime import date, time
from sqlalchemy.exc import IntegrityError, StatementError

from models.appointment import Appointment
from models.practitioner_profile import PracProfile
from models.schedule import Schedule

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
def appointment(db_session, prac):
    appointment = Appointment(
        practitioner=prac,
        status='confirmed',
        type='once'
    )

    db_session.add(appointment)
    db_session.commit()

    return appointment


@pytest.fixture
def schedule(db_session, appointment):
    schedule = Schedule(
        appointment=appointment,
        time_from=time(9, 30),
        time_to=time(9, 50),
        date=date(2020, 5, 1),
        status='complete'
    )
    db_session.add(schedule)
    db_session.commit()
    return schedule


def test_appointment_module_docstring():
    check_module_docstring(Schedule)


def test_schedule_creation(db_session, appointment):
    schedule = Schedule(
        appointment=appointment,
        date=date(2020, 5, 1),
        time_from=time(9, 30),
        time_to=time(9, 50),
        status='complete'
    )
    db_session.add(schedule)

    assert schedule.appointment == appointment
    assert schedule.date is not None
    assert schedule.id is not None
    assert schedule.created_at is not None
    assert schedule.updated_at is not None


def test_correct_enum(db_session, appointment):
    schedule = Schedule(
        appointment=appointment,
        date=date(2020, 5, 1),
        time_from=time(9, 30),
        time_to=time(9, 50),
        status='not valid'
    )
    db_session.add(schedule)
    with pytest.raises(StatementError):
        db_session.commit()
    db_session.rollback()


@pytest.mark.parametrize("field", ["appointment_id", "date", "time_from", "time_to",
                                   "status"])
def test_slot_missing_required_fields(db_session, field, appointment):
    """Test that missing required fields raises an IntegrityError."""
    kwargs = {
        "appointment_id": appointment.id,
        "date": date(2020, 5, 1),
        "time_from": time(9, 30),
        "time_to": time(9, 50),
        "status": "complete"
    }

    del kwargs[field]  # Remove the field being tested

    schedule = Schedule(**kwargs)

    db_session.add(schedule)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_deleting_schedule_removes_schedule_from_appointment_list(db_session,
                                                                  appointment):
    schedule1 = Schedule(
        appointment=appointment,
        time_from=time(9, 20),
        time_to=time(9, 40),
        date=date(2020, 5, 1),
        status='complete'
    )
    schedule2 = Schedule(
        appointment=appointment,
        time_from=time(9, 20),
        time_to=time(9, 40),
        date=date(2020, 5, 2),
        status='complete'
    )

    db_session.add_all([schedule1, schedule2])
    db_session.commit()

    assert db_session.query(Schedule).count() == 2
    assert len(appointment.schedules) == 2
    assert schedule1 in appointment.schedules
    assert schedule2 in appointment.schedules

    schedule1.delete()
    db_session.commit()
    assert len(appointment.schedules) == 1
    assert schedule2 in appointment.schedules
    assert db_session.query(Schedule).count() == 1

    schedule2.delete()
    db_session.commit()
    assert appointment.schedules == []
    assert db_session.query(Schedule).count() == 0
