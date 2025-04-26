from api.v1 import db
from models.base_model import BaseModel

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class LogInfo(UserMixin, BaseModel, db.Model):
    __tablename__ = 'loginfos'

    password_hash = db.Column(db.String(255), unique=True)
    account_type = db.Column(db.Enum('adult', 'child', 'practitioner', 'admin'))
    email = db.Column(db.String(60), index=True)
    acc_status = db.Column(db.Enum('unverified', 'verified', 'active',
                                   'inactive', 'deactivated'))
    prac_profile = db.relationship('PracProfile', back_populates='loginfo',
                                   uselist=False)
    adult_profile = db.relationship('AdultProfile', back_populates='loginfo',
                                    uselist=False)
    child_profile = db.relationship('ChildProfile', back_populates='loginfo',
                                    uselist=False,
                                    foreign_keys='ChildProfile.loginfo_id')
    created_children = db.relationship('ChildProfile',
                                       back_populates='created_by',
                                       foreign_keys='ChildProfile.created_by_id')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
