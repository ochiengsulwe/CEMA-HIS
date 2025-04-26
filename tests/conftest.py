"""
Defines common/shared fixtures, set-ups, and configurations for all tests.
"""
import inspect
import pytest

from api.v1 import create_app, db


@pytest.fixture(scope='session')
def test_app():
    """Creates an instance of a Flask app to be used in tests"""
    app = create_app('test')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def db_session(test_app):
    """Provides a clean transactional database session for tests"""
    with test_app.app_context():
        db.drop_all()
        db.create_all()
        try:
            yield db.session
        finally:
            db.session.rollback()
            db.session.remove()


@pytest.fixture(scope='module')
def test_client(test_app):
    """Provides a Flask test client for route testing."""
    return test_app.test_client()


def check_module_docstring(module):
    """Helper function to check if a module has a top-level docstring"""
    assert inspect.getdoc(module) is not \
        None, f"{module.__name__} should have a top-level docstring"
