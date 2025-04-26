"""
This module stipulates time spans
"""
from api.v1 import db
from models.base_model import BaseModel


class Span(BaseModel, db.Model):
    __tablename__ = 'spans'

    slot_id = db.Column(db.String(60), db.ForeignKey('slots.id', ondelete="CASCADE"),
                        nullable=False)
    time_from = db.Column(db.Time, nullable=False)
    time_to = db.Column(db.Time, nullable=False)

    slot = db.relationship('Slot', back_populates='spans', uselist=False)
