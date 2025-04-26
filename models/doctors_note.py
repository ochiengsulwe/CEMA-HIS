"""
Describes the notes a practitioner takes during diagnosis
"""
from api.v1 import db
from models.base_model import BaseModel


class DoctorNote(BaseModel, db.Model):
    """
    A Doctor's Note is informal guide to diagnosis.

    The Note will consist of two main attributes:
        i. Note - a summary of objective and subjective symptom analysis of symptoms
        ii. Assessment - a suggested condition to be confirmed by other later procedure
    """
    __tablename__ = 'doctors_notes'

    note = db.Column(db.Text, nullable=False)
    assessment = db.Column(db.Text, nullable=False)
    schedule_id = db.Column(db.String(60), db.ForeignKey('schedules.id',
                                                         ondelete='CASCADE'),
                            nullable=False)

    schedule = db.relationship('Schedule', back_populates='note', uselist=False)
