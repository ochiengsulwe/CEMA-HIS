"""
This is a table that holds all patient's prescription entries into one
"""
from api.v1 import db
from models.base_model import BaseModel


class PatientPrescription(BaseModel, db.Model):
    """
    The class is a more refined/collection of PrescriptionmEntry class into
        a single entry.

    This class merges all that a practitioner enters into the entry interface into one.
    This class has the following core attributes:
    i. schedule_id: holds bo the patient and practitioner data
    ii. status: issue status of the prescription to track it from practitioner to the
        issueng pharmacy.
    """
    __tablename__ = 'patient_prescriptions'

    schedule_id = db.Column(db.String(60), db.ForeignKey('schedules.id',
                                                         ondelete='CASCADE'),
                            nullable=False)
    status = db.Column(db.Enum('draft', 'issued', 'received', 'fulfilled',
                               'cancelled'), default='draft')

    schedule = db.relationship('Schedule', back_populates='prescription', uselist=False)
    pre_entries = db.relationship('PrescriptionEntry', back_populates='prescription',
                                  cascade='all, delete-orphan')
