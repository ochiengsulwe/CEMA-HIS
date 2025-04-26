import pytest

from datetime import date, time
# from sqlalchemy.exc import IntegrityError

from models.planner import Planner
from models.practitioner_profile import PracProfile
from models.slot import Slot
from models.span import Span

# from tests.conftest import check_module_docstring
from utils.adjust_free_time import delete_exact_match


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
        time_from=time(9, 30),
        time_to=time(9, 50)
    )
    db_session.add(span)
    db_session.commit()

    return span


def test_delete_span_from_db(db_session, span):
    assert db_session.query(Span).count() == 1
    delete_exact_match(span)
    db_session.commit()
    assert db_session.query(Span).count() == 0
