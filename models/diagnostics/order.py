"""
Describes the Test order anatomy
"""
from api.v1 import db
from models.base_model import BaseModel


class TestOrder(BaseModel, db.Model):
    """
    Outlines what every Test order should have to be used for system circulation
    """
    __tablename__ = 'test_orders'

    schedule_id = db.Column(db.String(60),
                            db.ForeignKey('schedules.id', ondelete='CASCADE'),
                            nullable=False)
    test_id = db.Column(db.String(60),
                        db.ForeignKey('diagnostic_tests.id', ondelete='CASCADE'),
                        nullable=False)
    status = db.Column(db.Enum('ordered', 'received', 'cancelled', 'completed'),
                       default='ordered')
    result = db.Column(db.Text)

    schedule = db.relationship('Schedule', back_populates='test_orders', uselist=False)

    test_links = db.relationship("TestOrderTestLink", back_populates="test_order",
                                 cascade="all, delete-orphan")

    # Shortcut for easy access to tests
    diagnostic_tests = db.relationship(
        "DiagnosticTest",
        secondary="test_order_test_link",
        viewonly=True,
        back_populates="test_orders"
    )
