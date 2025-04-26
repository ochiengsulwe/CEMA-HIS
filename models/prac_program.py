"""
This Class initialises a relationship bewteen the availbale programs, practitioners who
    run them, and patients who are involved in them.
"""
from models.base_model import BaseModel
from api.v1 import db


class PractitionerProgram(BaseModel, db.Model):

    __tablename__ = 'practitioner_programs'

    program_id = db.Column(db.String(60), db.ForeignKey('health_programs.id',
                                                        ondelete='CASCADE'),
                           nullable=False)
    prac_id = db.Column(db.String(60), db.ForeignKey('prac_profiles.id',
                                                     ondelete='CASCADE'),
                        nullable=False)
    program = db.relationship('HealthProgram', back_populates='prac_programs',
                              uselist=False)
    practitioner = db.relationship('PracProfile', back_populates='programs',
                                   uselist='False')
    enrolled_adults = db.relationship(
        'AdultProfile',
        secondary='adult_program_enrollments',
        back_populates='enrolled_programs'
    )
    enrolled_children = db.relationship(
        'ChildProfile',
        secondary='child_program_enrollments',
        back_populates='enrolled_programs'
    )
