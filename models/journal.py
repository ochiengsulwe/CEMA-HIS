from models.base_model import BaseModel
from api.v1 import db


class Journal(BaseModel, db.Model):
    __tablename__ = 'journals'

    body = db.Column(db.Text)
    adult_id = db.Column(db.String(60), db.ForeignKey('adult_profiles.id'))
    child_id = db.Column(db.String(60), db.ForeignKey('child_profiles.id'))
    journaled_by_id = db.Column(db.String(60), db.ForeignKey('adult_profiles.id'))

    child_profile = db.relationship('ChildProfile', back_populates='journals')
    adult_profile = db.relationship('AdultProfile', foreign_keys=[adult_id],
                                    back_populates='journals')
    journaled_by = db.relationship('AdultProfile', foreign_keys=[journaled_by_id],
                                   back_populates='journals_created')
