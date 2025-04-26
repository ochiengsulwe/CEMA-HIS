from api.v1 import db
from models.base_model import BaseModel


class Date(BaseModel, db.Model):
    """Represents a date with additional attributes."""
    __tablename__ = 'dates'

    day = db.Column(db.String(15), nullable=False)  # Full name (e.g., 'Monday')
    date = db.Column(db.Date, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.CheckConstraint('month BETWEEN 1 AND 12', name='valid_month'),
        db.CheckConstraint('year >= 1', name='valid_year'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'date' in kwargs:
            self.date = kwargs['date']
            self.day = self.calculate_day_of_week(self.date)
            self.year = self.date.year
            self.month = self.date.month
        else:
            raise ValueError("Date field is required")

    @staticmethod
    def calculate_day_of_week(date):
        """Calculate and return the day of the week for the given date."""
        return date.strftime('%A')  # Returns full day name (e.g., 'Monday')
