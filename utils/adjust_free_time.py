"""
This module deals with slot methods.

The nethods which include partitioning, chunking and adjustment, depending on the
    presented circumstance.
"""
from datetime import datetime, timedelta

from models.span import Span


def delete_exact_match(span):
    """
    Deletes a free time slot of the exact match as the appointment time.

    Args:
        span (:obj:`class`): The span to be compared against the appointment schedule.

    """
    span.delete()


def adjust_span(span, time_to):
    """
    Adjusts practitioner's slot if the appointment time_from mataches slot's time_to.

    Args:
        span (obj): The span to be adjusted accordingly.
        time_to (datetime.time): Appointment's time_to. This will be the new span's
            time_from.
    """
    now = datetime.combine(datetime.today(), time_to)
    span.time_from = (now + timedelta(minutes=5)).time()


def adjust_span_end(span, time_from):
    """
    Adjusts the practitioner availability to match the appointment start time.

    This method makes sure that new end time matches the start time of appointment.

    Args:
        span (obj): practitioner availability
        time_from (datetime.time): appointment start time
    """
    now = datetime.combine(datetime.today(), time_from)
    span.time_to = (now - timedelta(minutes=5)).time()


def split_span(span, time_from, time_to):
    """
    Splits the slot if appointmentment time falls in between the slot time.

    What this does, it breaks the practitioner's slot into two, chunking out the
        appointment time from the slot.

    Args:
        span (obj): Practioner's slot time span
        time_from (datetime.time): Appointment starting time.
        time_to (datetime.time): Appointment end time.
    """
    fro = datetime.combine(datetime.today(), time_from)
    to = datetime.combine(datetime.today(), time_to)
    updated_spans = [
        Span(slot_id=span.slot_id, time_from=span.time_from,
             time_to=(fro - timedelta(minutes=5)).time()),
        Span(slot_id=span.slot_id,
             time_from=(to + timedelta(minutes=5)).time(), time_to=span.time_to)
             ]
    span.delete()

    for sp in updated_spans:
        sp.save()


def adjust_planner(free, time_from, time_to):
    """
    Adjusts a practitioner's planner accordingly depending on the appointment time.

    Args:
        free (obj): Practitioner's availability found from planner (span).
        time_from (datetime.time): Appointment starting time.
        time_to (datetime.time): Appointment end time.
    """
    if time_from == free.time_from:
        if time_to == free.time_to:
            delete_exact_match(free)
        else:
            adjust_span(free, time_to)
    elif time_to == free.time_to:
        adjust_span_end(free, time_from)
    elif (free.time_from < time_from < free.time_to and free.time_from < time_to <
          free.time_to):
        split_span(free, time_from, time_to)
