"""
Describes channel through which a practitioner can enter prescriptions into the system
"""
from api.v1 import db
from models.base_model import BaseModel


class PrescriptionEntry(BaseModel, db.Model):
    """
    PrescriptionEntry class is the system entry point of patients' prescription

    PrescriptionEntry is more of a collection funnel, where prescriptions filter through

    It is made of core attributes:
    i. category: what is being prescribed => medication, vaccination etc
    ii. sub_category: if medication (or any other), what type of medication (injection)
    iii. name: this holds the name of the sub_category object selected
    iv. note: more of instructions of taking the prescription
    v. frequency: this isa relatiosnship for time spans and frequency of prescription
    """
    __tablename__ = 'prescription_entries'

    category = db.Column(db.Enum('medication', 'vaccination', 'chemotherapy',
                                 'psychotherapy', 'therapy', 'medical_device',
                                 'radiotherapy', 'dialysis', 'nutritional_support',
                                 'immunotherapy', 'surgery', 'rehabilitation'),
                         nullable=False)
    sub_category = db.Column(db.String(60))
    name = db.Column(db.String(60), nullable=False)
    note = db.Column(db.Text)
    prescription_id = db.Column(db.String(60),
                                db.ForeignKey('patient_prescriptions.id',
                                              ondelete='CASCADE'), nullable=False)
    frequency = db.relationship('Frequency', back_populates='prescription_entry',
                                uselist=False, cascade='all, delete-orphan')
    prescription = db.relationship('PatientPrescription', back_populates='pre_entries',
                                   uselist=False)
