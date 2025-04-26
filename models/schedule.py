"""
Tracks patient's appointment bookinigs.

A patient can only have one appointmnet entry with the same practiitoner.
If multiple is needed, the status has to change to recurrent in the Appointment table.
"""
from api.v1 import db
from models.base_model import BaseModel


class Schedule(BaseModel, db.Model):
    """Represents a schedule for appointments."""
    __tablename__ = 'schedules'
    appointment_id = db.Column(db.String(60), db.ForeignKey('appointments.id',
                                                            ondelete='CASCADE'),
                               nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_from = db.Column(db.Time, nullable=False)
    time_to = db.Column(db.Time, nullable=False)
    status = db.Column(db.Enum('complete', 'pending'), nullable=False)
    span_next_day = db.Column(db.Boolean, default=False)

    appointment = db.relationship('Appointment', back_populates='schedules',
                                  uselist=False)
    test_orders = db.relationship('TestOrder', back_populates='schedule',
                                  cascade='all, delete-orphan')
    note = db.relationship('DoctorNote', back_populates='schedule',
                           uselist=False, cascade='all, delete-orphan')
    diagnosis = db.relationship('Diagnosis', back_populates='schedule',
                                uselist=False, cascade='all, delete-orphan')
    prescription = db.relationship('PatientPrescription', back_populates='schedule',
                                   cascade='all, delete-orphan', uselist=False)
