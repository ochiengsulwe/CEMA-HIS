from api.v1 import db
from models.base_model import BaseModel


class Planner(BaseModel, db.Model):
    """Represents a planner.

       The planner represents the free time a practitioner has in a day
    """
    __tablename__ = 'planners'

    prac_profile_id = db.Column(db.String(60), db.ForeignKey('prac_profiles.id'),
                                nullable=False, unique=True)

    practitioner = db.relationship('PracProfile', back_populates='planner',
                                   uselist=False)
    slots = db.relationship('Slot', back_populates='planner',
                            cascade="all, delete-orphan")
