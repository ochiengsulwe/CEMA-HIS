"""This module tracks the free time a practitioner has.

With every appointment in a day, the free time is reduced by the appointment time.
It works hand in hand with the Schedule Class.
"""
from api.v1 import db
from models.base_model import BaseModel


class Slot(BaseModel, db.Model):
    __tablename__ = 'slots'

    date = db.Column(db.Date, nullable=False)
    planner_id = db.Column(db.String(60),
                           db.ForeignKey('planners.id', ondelete="CASCADE"),
                           nullable=False)

    planner = db.relationship('Planner', back_populates='slots')
    spans = db.relationship('Span', back_populates='slot', cascade="all, delete-orphan")
