"""
Describes a practitioner's analysis and findings from patient's symptoms
"""
from api.v1 import db
from models.base_model import BaseModel


class Diagnosis(BaseModel, db.Model):
    """
    Diagnosis is more of a finding coupled with recommendations

    Diagnosis class has three core attributes:
    i. diagnosis: the finding, majorly from diagnostic tests or from cross-examination
    ii. severity: how bad the findings are depending on the test results
    iii. prognosis: the recommendation of what to do next for full recovery
    """
    __tablename__ = 'diagnoses'

    diagnosis = db.Column(db.Text, nullable=False)
    severity = db.Column(db.Enum('mild', 'moderate', 'severe'), nullable=False)
    prognosis = db.Column(db.Text, nullable=False)
    schedule_id = db.Column(db.String(60), db.ForeignKey('schedules.id',
                                                         ondelete='CASCADE'),
                            nullable=False)
    schedule = db.relationship('Schedule', back_populates='diagnosis', uselist=False)
