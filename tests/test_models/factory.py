"""
This module defines object factories to be used in various tests.
"""
import factory
import uuid
from datetime import datetime, timedelta

from models.appointment import Appointment
from models.planner import Planner
from models.practitioner_profile import PracProfile
from models.schedule import Schedule
from models.slot import Slot
from models.span import Span


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop("session", None)

        if session is None:
            raise ValueError(
                "Session must be explicitly provided:SpanFactory(session=db_session)"
            )

        cls._meta.sqlalchemy_session = session
        obj = super()._create(model_class, *args, **kwargs)
        session.add(obj)
        session.flush()
        return obj


class PractitionerFactory(BaseFactory):
    class Meta:
        model = PracProfile
        # sqlalchemy_session_persistence = "flush"

    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    bio = factory.Faker('paragraph')
    fee = factory.Faker('random_int', min=500, max=5000)
    phone_number = factory.Faker('phone_number')
    profession_reg = factory.Faker('uuid4')
    prof_reg_year = factory.Faker('date_between', start_date="-30y", end_date="today")
    profession = factory.Iterator(['General Practitioner', 'Pediatrician',
                                   'Dermatologist'])
    specialization = factory.Iterator(['Cardiology', 'Neurology', 'None'])
    specialization_reg = factory.Faker('uuid4')
    spec_reg_year = factory.Maybe(
        'specialization',  # Generate only if specialization is not "None"
        yes_declaration=factory.Faker('date_between', start_date="-20y",
                                      end_date="today"),
        no_declaration=None,
    )
    """
    loginfo = factory.SubFactory(LoginfoFactory)  # Ensure this factory exists
    identity = factory.SubFactory(UserFactory)  # Ensure this factory exists
    """


class AppointmentFactory(BaseFactory):
    class Meta:
        model = Appointment
        # sqlalchemy_session_persistence = "commit" #Ensure it commits for relationships
        # sqlalchemy_session_persistence = "flush"  # Keeps objects in memory

    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    status = factory.Iterator(['confirmed', 'cancelled', 'pending'])
    type = factory.Iterator(['once', 'repeat'])
    practitioner = factory.SubFactory(PractitionerFactory)


class ScheduleFactory(BaseFactory):
    class Meta:
        model = Schedule
        # sqlalchemy_session_persistence = "flush"

    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    appointment = factory.SubFactory(AppointmentFactory)
    date = factory.Faker('date_object')
    status = factory.Iterator(['complete', 'pending'])
    time_from = factory.LazyFunction(
        lambda: datetime.utcnow().replace(second=0, microsecond=0).time())
    time_to = factory.LazyFunction(
        lambda: (datetime.utcnow() + timedelta(minutes=30)).replace(
            second=0, microsecond=0).time())


class PlannerFactory(BaseFactory):
    class Meta:
        model = Planner

        # sqlalchemy_session_persistence = "flush"

    practitioner = factory.SubFactory(PractitionerFactory)


class SlotFactory(BaseFactory):
    class Meta:
        model = Slot
        sqlalchemy_session_persistence = "flush"

    date = factory.Faker('date_object')
    planner = factory.SubFactory(PlannerFactory)


class SpanFactory(BaseFactory):
    class Meta:
        model = Span
        # sqlalchemy_session_persistence = "flush"

    slot_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    time_from = factory.LazyFunction(
        lambda: datetime.utcnow().replace(second=0, microsecond=0).time()
    )
    time_to = factory.LazyFunction(
        lambda: (datetime.utcnow() + timedelta(minutes=30)).replace(
            second=0, microsecond=0).time()
    )
    slot = factory.SubFactory(SlotFactory)
