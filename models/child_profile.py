from api.v1 import db
from models.base_model import BaseModel

family = db.Table('family',
                  db.Column('child_id', db.String(60),
                            db.ForeignKey('child_profiles.id',
                                          onupdate='CASCADE',
                                          ondelete='CASCADE'),
                            primary_key=True),
                  db.Column('parent_id', db.String(60),
                            db.ForeignKey('adult_profiles.id',
                                          ondelete='CASCADE',
                                          onupdate='CASCADE'),
                            primary_key=True))


child_program_enrollments = db.Table(
    'child_program_enrollments',
    db.Column('child_id', db.String(60),
              db.ForeignKey('child_profiles.id'), primary_key=True),
    db.Column('practitioner_program_id', db.String(60),
              db.ForeignKey('practitioner_programs.id'), primary_key=True)
)


class ChildProfile(BaseModel, db.Model):

    __tablename__ = 'child_profiles'

    loginfo_id = db.Column(db.String(60), db.ForeignKey('loginfos.id'))
    created_by_id = db.Column(db.String(60), db.ForeignKey('loginfos.id'))
    identity_id = db.Column(db.String(60), db.ForeignKey('users.id'))

    identity = db.relationship('User', back_populates='child', uselist=False)
    created_by = db.relationship('LogInfo', foreign_keys=[created_by_id],
                                 back_populates='created_children', uselist=False)
    loginfo = db.relationship('LogInfo', foreign_keys=[loginfo_id],
                              back_populates='child_profile',
                              uselist=False)
    parents = db.relationship('AdultProfile', secondary=family,
                              back_populates='children')
    appointments = db.relationship('Appointment', back_populates='child_profile')
    enrolled_programs = db.relationship(
        'PractitionerProgram',
        secondary='child_program_enrollments',
        back_populates='enrolled_children'
    )
