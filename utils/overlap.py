"""
This module checks if there is an overlap in time.
"""


def schedule_overlap(user, date, time_from, time_to):
    """
    Checks for overlaps in appointment schedules.

    Args:
        user (obj): The user to check appointment schedule overlap
        date (datetime.date): The appoinment date
        time_from (datetime.time): The appointment start time
        time_to (datetime.time): The appointment end time

    Returns:
        obj: Returns the overlapping schedule if found or None
    """

    new_s = next(
        (
            appt for appt in user.appointments
            for appt_schedule in appt.schedules
            if appt_schedule.date == date and
            not (appt_schedule.time_to <= time_from or
                 appt_schedule.time_from >= time_to)
        ),
        None
    )
    return new_s


def span_find(prac, date, time_from, time_to):
    """
    Finds the actual span to allocate new appointment time from

    Args:
        prac (obj): The practitioner to check span from
        date (datetime.date): The appointment date
        time_from (datetime.time): The appointment time
        time_to (datetime.time): The appointment time

    Returns:
        obj: The found span object or None if not found
    """

    free = next(
        (
            sp for sl in prac.planner.slots if sl.date == date for sp in
            sl.spans if sp.time_from <= time_from and sp.time_to >= time_to
        ),
        None
    )
    return free


def date_find(prac, date):
    """
    Checks if a planner has a specific date to it.

    Args:
        prac (obj): A PracProfile object with the practitioner information
        date (datetime.date): the date to find

    Returns:
        bool: True if date exist or False if not found
    """
    response = next(
        (
         sl for sl in prac.planner.slots if sl.date == date
        ),
        None
    )
    return response is not None


def check_schedule(session, prac, date, time_from, time_to):
    """
    Adjusts practitioner's planner by removing overlapping scheduled appointments.

    Makes sure a practitioner doesn't create a free time considing with an existing
        appointment with a patient

    Args:
        session (Session): current db session
        prac (obj): PracProfile instance
        date (datetime.date): the date to check
        time_from (datetime.time): starting time
        time_to (datetime.time): ending time

    Returns:
        list: a list of free times excluding overlaps, with interludes
        or error if entire slot is taken.
    """
    from datetime import datetime, timedelta
    from flask import jsonify
    from sqlalchemy import and_

    from models.schedule import Schedule

    schedules = Schedule.query.filter(
        and_(
            Schedule.date == date,
            Schedule.appointment.has(practitioner=prac)
        )
    ).all()

    buffer = timedelta(minutes=5)
    base_start = datetime.combine(date, time_from)
    base_end = datetime.combine(date, time_to)

    # Start with entire proposed range
    available_spans = [(base_start, base_end)]

    # Sort schedules for clean processing
    schedules.sort(key=lambda s: s.time_from)

    for s in schedules:
        sched_start = datetime.combine(date, s.time_from)
        sched_end = datetime.combine(date, s.time_to)

        # Exact match OR proposed time fully engulfed by appointment (with buffer)
        if sched_start - buffer <= base_start and sched_end + buffer >= base_end:
            return jsonify({'error': 'you have an appointment at this time'}), 409

        new_spans = []

        for span_start, span_end in available_spans:
            # No overlap
            if sched_end + buffer <= span_start or sched_start - buffer >= span_end:
                new_spans.append((span_start, span_end))
            else:
                # Overlap: cut before and/or after
                if sched_start - buffer > span_start:
                    new_spans.append((span_start, sched_start - buffer))
                if sched_end + buffer < span_end:
                    new_spans.append((sched_end + buffer, span_end))

        available_spans = new_spans

    # Filter out too-small slots if needed, and format
    span_list = [
        {
            "time_from": span[0].time().strftime("%H:%M"),
            "time_to": span[1].time().strftime("%H:%M")
        }
        for span in available_spans if span[1] > span[0]
    ]

    return span_list
