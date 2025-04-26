"""
Describes how prescription is to be taken.

Outlines the timeframes, intervals of administrations, when to start and when to end.

This is to be used mainly with a `Pharmacist` object of the `Practitioner` class
"""

from api.v1 import db
from models.base_model import BaseModel
from datetime import timedelta
from sqlalchemy import JSON


class Frequency(BaseModel, db.Model):
    """
    Frequency class tracks time attribute of every prescription.

    Attributes:
    - start_date: Date the prescription administration starts.
    - end_date: Date the prescription ends (computed).
    - routine: Interval of administration (daily, weekly, monthly, once).
    - times: How many times to administer within the selected interval.
    - duration: For how long the prescription should be administered.
    - for_: Units of duration (days, weeks, months).
    - start_time: Exact time the first administration is to begin.
    - at_: A list of time strings (HH:MM:SS) when prescription is to be taken.
    """

    __tablename__ = 'frequencies'

    start_date = db.Column(db.Date, nullable=False)
    _end_date = db.Column("end_date", db.Date, nullable=True)
    routine = db.Column(db.Enum('daily', 'monthly', 'once', 'weekly'), nullable=False)
    times = db.Column(db.Integer, nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    for_ = db.Column(db.Enum('days', 'months', 'weeks'), nullable=True)
    start_time = db.Column(db.Time, nullable=False)
    at_ = db.Column(JSON, nullable=True)
    prescription_id = db.Column(db.String(60), db.ForeignKey('prescription_entries.id',
                                                             ondelete='CASCADE'),
                                nullable=False)

    prescription_entry = db.relationship('PrescriptionEntry',
                                         back_populates='frequency', uselist=False)

    @property
    def end_date(self):
        """Compute the end date from start_date and duration"""
        if self.start_date and self.routine:
            if self.routine == 'once':
                return self.start_date
            if self.duration and self.for_:
                if self.for_ == 'days':
                    return self.start_date + timedelta(days=self.duration)
                if self.for_ == 'weeks':
                    return self.start_date + timedelta(weeks=self.duration)
                if self.for_ == 'months':
                    return self.start_date + timedelta(days=30 * self.duration)
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = value

    def generate_times(self):
        if not self.start_time or not self.times or self.times < 1:
            return []

        spacing = int(24 * 60 / self.times)
        start_minutes = self.start_time.hour * 60 + self.start_time.minute
        times_list = []

        for i in range(self.times):
            total_minutes = (start_minutes + i * spacing) % (24 * 60)
            hour = total_minutes // 60
            minute = total_minutes % 60
            times_list.append(f"{hour:02d}:{minute:02d}:00")

        return times_list

    def save(self, *args, **kwargs):
        if not self.at_:
            self.at_ = self.generate_times()
        if not self._end_date:
            self._end_date = self.end_date
        super().save(*args, **kwargs)
