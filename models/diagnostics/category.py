"""
This class defines the overall diagnotistic test available
"""
from api.v1 import db
from models.base_model import BaseModel


class DiagnosticCategory(BaseModel, db.Model):
    """
    Diagnostic test search will begin from here.
    """
    __tablename__ = 'diagnostic_categories'

    name = db.Column(db.String(255), nullable=False)  # Laboratory test, Image test
    tests = db.relationship('DiagnosticTest', back_populates='category',
                            cascade="all, delete-orphan")
