"""This model class describes unique features to an adult account.

Here also the relationships between child/parent are defined, as well as
next-of-kin relationships.
"""

from api.v1 import db
from models.base_model import BaseModel
from models.child_profile import family


adult_program_enrollments = db.Table(
    'adult_program_enrollments',
    db.Column('adult_id', db.String(60),
              db.ForeignKey('adult_profiles.id'), primary_key=True),
    db.Column('practitioner_program_id', db.String(60),
              db.ForeignKey('practitioner_programs.id'), primary_key=True)
)


class AdultProfile(BaseModel, db.Model):

    __tablename__ = 'adult_profiles'

    phone_number = db.Column(db.String(16), unique=True)
    '''To be picked from the National ID Database( Sub-location field)'''
    permanent_location = db.Column(db.String(60), nullable=False)
    current_location = db.Column(db.String(60))
    loginfo_id = db.Column(db.String(60), db.ForeignKey('loginfos.id'))
    identity_id = db.Column(db.String(60), db.ForeignKey('users.id'))
    next_of_kin_id = db.Column(db.String(60),
                               db.ForeignKey('adult_profiles.id'))

    identity = db.relationship('User', back_populates='adult', uselist=False)
    dependents = db.relationship('AdultProfile', back_populates='next_of_kin')
    next_of_kin = db.relationship('AdultProfile',
                                  back_populates='dependents',
                                  remote_side='AdultProfile.id')
    loginfo = db.relationship('LogInfo', back_populates='adult_profile',
                              uselist=False)
    children = db.relationship('ChildProfile', secondary=family,
                               back_populates='parents')
    appointments = db.relationship('Appointment', back_populates='adult_profile')
    enrolled_programs = db.relationship(
        'PractitionerProgram',
        secondary='adult_program_enrollments',
        back_populates='enrolled_adults'
    )
