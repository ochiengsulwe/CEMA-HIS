"""The model describes the user class.
 This calss will be used to count the total number of the system users.
 Every user will only be registered once to the users table.
"""
from datetime import date
from flask_login import AnonymousUserMixin
from api.v1 import db
from models.base_model import BaseModel


class User(BaseModel, db.Model):
    """
    holds the user data model definition
        - fields
        - user manipulation methods
    """

    __tablename__ = "users"

    first_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.Enum('Female', 'Male'), nullable=False)
    date_of_birth = db.Column(db.Date)
    birth_cert_number = db.Column(db.Integer, unique=True,
                                  index=True)
    id_number = db.Column(db.Integer, index=True, unique=True)
    passport_number = db.Column(db.String(16), unique=True, index=True)
    child = db.relationship('ChildProfile', back_populates='identity', uselist=False)
    adult = db.relationship('AdultProfile', back_populates='identity', uselist=False)
    practitioner = db.relationship('PracProfile', back_populates='identity',
                                   uselist=False)

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month,
                                           self.date_of_birth.day):
                age -= 1
            return age
        return None


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False
