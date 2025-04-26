"""Describes the appointment details of a patient in realtion to the
    practiioner.
"""
# from models.schedule import appointment_schedules
from models.base_model import BaseModel
from api.v1 import db


class Appointment(BaseModel, db.Model):
    __tablename__ = 'appointments'

    child_id = db.Column(db.String(60), db.ForeignKey('child_profiles.id'))
    adult_id = db.Column(db.String(60), db.ForeignKey('adult_profiles.id'))
    practitioner_id = db.Column(db.String(60), db.ForeignKey('prac_profiles.id'),
                                nullable=False)
    status = db.Column(db.Enum('confirmed', 'cancelled', 'pending'), nullable=False)
    type = db.Column(db.Enum('once', 'repeat'), nullable=False)
    program_id = db.Column(db.String(60), db.ForeignKey('health_programs.id',
                                                        ondelete='CASCADE'))

    child_profile = db.relationship('ChildProfile', back_populates='appointments',
                                    uselist=False)
    adult_profile = db.relationship('AdultProfile', back_populates='appointments',
                                    uselist=False)
    practitioner = db.relationship('PracProfile', back_populates='appointments',
                                   uselist=False)
    schedules = db.relationship('Schedule', back_populates='appointment',
                                cascade='all, delete-orphan')
    program = db.relationship('HealthProgram', back_populates='appointments',
                              uselist=False)
