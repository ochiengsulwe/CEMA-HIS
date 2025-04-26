"""
This is an association model/object that establishes a conection between TestOrder and
    DiagnosticTest tables in a many-to-many relationshhip
"""
from api.v1 import db
from models.base_model import BaseModel


class TestOrderTestLink(BaseModel, db.Model):
    """ Accociation model for TestOrder and DiagnosticTest"""

    __tablename__ = 'test_order_test_link'

    test_order_id = db.Column(db.String(60), db.ForeignKey('test_orders.id',
                                                           ondelete='CASCADE'),
                              primary_key=True)
    diagnostic_test_id = db.Column(db.String(60), db.ForeignKey('diagnostic_tests.id',
                                                                ondelete='CASCADE'),
                                   primary_key=True)

    result = db.Column(db.Text)
    status = db.Column(db.Enum('complete', 'waiting'), nullable=False,
                       default='waiting')

    test_order = db.relationship("TestOrder", back_populates="test_links")
    diagnostic_test = db.relationship("DiagnosticTest", back_populates="order_links")
