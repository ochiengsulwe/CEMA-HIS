"""
This model describes all abvailable programmes available/managed within the system.

From these, a practitioner may choose any/even all to run depending on their
    specialization
"""
from api.v1 import db
from models.base_model import BaseModel


class HealthProgram(BaseModel, db.Model):
    __tablename__ = 'health_programs'

    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text)

    prac_programs = db.relationship('PractitionerProgram', back_populates='program',
                                    cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', back_populates='program',
                                   cascade='all, delete-orphan')
