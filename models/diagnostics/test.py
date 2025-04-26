"""
Describes the specific test to be done
"""
from api.v1 import db
from models.base_model import BaseModel


class DiagnosticTest(BaseModel, db.Model):
    """
    Holds the actusl tests to be done on a patient
    """
    __tablename__ = "diagnostic_tests"

    name = db.Column(db.String(255), nullable=False)
    test_for = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.String(60),
                            db.ForeignKey('diagnostic_categories.id',
                                          ondelete='CASCADE'),
                            nullable=False)
    category = db.relationship('DiagnosticCategory', back_populates='tests')
    order_links = db.relationship("TestOrderTestLink",
                                  back_populates="diagnostic_test",
                                  cascade="all, delete-orphan")

    # Shortcut for easy access to test orders
    test_orders = db.relationship(
        "TestOrder",
        secondary="test_order_test_link",
        viewonly=True,
        back_populates="diagnostic_tests"
    )
