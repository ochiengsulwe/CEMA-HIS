from datetime import time
from api.v1 import db
from models.base_model import BaseModel

day_times = db.Table('day_times', db.Model.metadata,
                     db.Column('saa_id', db.ForeignKey('masaa.id'), primary_key=True),
                     db.Column('date_id', db.ForeignKey('dates.id'), primary_key=True)
                     )


class Saa(BaseModel, db.Model):
    """Represents a time with a single attribute `saa`."""
    __tablename__ = 'masaa'

    # A single column for the time in HH:MM format
    saa = db.Column(db.Time, nullable=False, unique=True)

    def __init__(self, hour, minute):
        # Set the time value from hour and minute
        self.saa = time(hour, minute)
