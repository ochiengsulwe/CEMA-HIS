"""Describes the table for level of discomfort"""
from api.v1 import db
from models.base_model import BaseModel


class Severity(BaseModel, db.Model):
    __tablename__ = 'severities'

    severity_level = db.Column(db.Enum("Mild", "Moderate", "Severe"),
                               nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    # patients = db.relationship('Allergy', back_populates='allergen')
