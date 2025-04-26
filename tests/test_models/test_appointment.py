
import pytest

from datetime import date, time
from sqlalchemy.exc import DataError, IntegrityError, StatementError

from models.appointment import Appointment
# from models.adult_profile import AdultProfile
# from models.child_profile import ChildProfile
from models.practitioner_profile import PracProfile
from models.schedule import Schedule

from tests.conftest import check_module_docstring
# from tests.test_models.factory import AppointmentFactory, ScheduleFactory

"""
@pytest.fixture
def schedule_factory(db_session):
    Factory function to create schedules.
    def _schedule_factory(**kwargs):
        return ScheduleFactory(**kwargs)

    return _schedule_factory
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
        status='confirmed',
        type='once'
    )
    schedule = Schedule(
        appointment=appointment,
        date=date(2020, 5, 1),
        status='pending',
        time_from=time(9, 20),
        time_to=time(9, 50)
    )

    db_session.add(appointment)
    db_session.add(schedule)
    db_session.commit()

    return appointment


def test_appointment_module_docstring():
    check_module_docstring(Appointment)


def test_appointment_creation(db_session, prac):
    appp = Appointment(
        adult_id='1234',
        practitioner_id=prac.id,
        status='confirmed',
        type='once'
    )
    db_session.add(appp)

    assert appp.practitioner_id == prac.id
    assert appp.status == 'confirmed'
    assert appp.type == 'once'
    assert appp.adult_id == '1234'
    assert appp.id is not None
    assert appp.created_at is not None
    assert appp.updated_at is not None


@pytest.mark.parametrize("status, type",
                         [
                             ("confirmed", "invalid"),
                             ("invalid", "once"),
                             ("pending", "wait"),
                             ("wrong", "repeat"),
                             ("cancelled", "nope"),
                         ])
def test_appointment_correct_enum(db_session, prac, status, type):
    appointment = Appointment(
        practitioner_id=prac.id,
        status=status,
        type=type
    )
    db_session.add(appointment)
    with pytest.raises((DataError, IntegrityError, StatementError)):
        db_session.commit()
    db_session.rollback()


@pytest.mark.parametrize("field", ["practitioner_id", "status", "type"])
def test_appointment_missing_required_fields(db_session, field):
    """Test that missing required fields raises an IntegrityError."""
    kwargs = {
        "practitioner_id": "12345",
        "status": "confirmed",
        "type": "once"
    }

    del kwargs[field]  # Remove the field being tested

    appointment = Appointment(**kwargs)

    db_session.add(appointment)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_appointment_can_have_multiple_schedules(db_session, appointment):
    """Test that an appointment can be associated with multiple schedules."""

    schedule1 = Schedule(
        appointment=appointment,
        date=date(2020, 5, 1),
        status='pending',
        time_from=time(9, 20),
        time_to=time(9, 40)
    )
    schedule2 = Schedule(
        appointment=appointment,
        date=date(2020, 5, 2),
        status='pending',
        time_from=time(9, 20),
        time_to=time(9, 40)
    )

    db_session.add_all([schedule1, schedule2])
    db_session.commit()

    assert len(appointment.schedules) == 3
    assert schedule1 in appointment.schedules
    assert schedule2 in appointment.schedules


def test_deleting_appointment_deletes_schedules(db_session, appointment):
    """Test that deleting an appointment deletes related schedules
        due to cascade delete."""

    schedule1 = Schedule(
        appointment=appointment,
        date=date(2020, 5, 1),
        status='pending',
        time_from=time(9, 20),
        time_to=time(9, 40)

    )
    schedule2 = Schedule(
        appointment=appointment,
        date=date(2020, 5, 2),
        status='pending',
        time_from=time(9, 20),
        time_to=time(9, 40)
    )

    db_session.add_all([schedule1, schedule2])
    db_session.commit()

    assert db_session.query(Schedule).count() == 3

    db_session.delete(appointment)
    db_session.commit()

    # Schedules should be deleted due to cascade
    assert db_session.query(Schedule).count() == 0
