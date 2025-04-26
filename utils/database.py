import re
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError


def check_email_exists(session_, model_class, email, account_type):
    """
    Check if an email exists for a specific account type in the LogInfo table.

    Args:
        email (str): The email to check.
        account_type (str): The account type to check.
        session (obj): The current sqlalchemy session.

    Returns:
        bool: True if the email exists for the given account type, False otherwise.
    """
    existing_entry = session_.query(
                                   model_class).filter_by(email=email,
                                                          account_type=account_type
                                                          ).first()
    return existing_entry is not None


def record_integrity(session, model_class, **kwargs):
    """Checks for duplicate values within the same account type.

        Works same as the UNIQUE SQL constraint, with a slight difference of
        checking for duplicates not in table but in account type.

        Args:
            sesssion (obj): the database instance in the current_app session.
            model_class (class): the class defining the table the check is to be
                                 done.
            **kwargs: a dictionary or key/value to be unpacked to table
                                 attributes and their respective values.

        Returns:
            obj: on success it returns an object, new entry to the database, or
                    throws an error, without writing to database.

====================================================================================
    AS LONG AS YOU ARE WRITING TO THE DATABASE, NEVER FORGET TO CALL THIS METHOD!
====================================================================================
    """
    try:
        record = model_class(**kwargs)
        session.add(record)
        session.flush()
        return record
    except (IntegrityError, FlushError) as e:
        session.rollback()
        # Extract the attribute name and value causing the duplication
        error_msg = str(e.orig)
        print("Error message:", error_msg)  # Debugging statement
        match = re.search(r"Duplicate entry '([^']+)' for key '.*?\.(\w+)'", error_msg)
        if match:
            attribute = match.group(2)
            value = match.group(1)
            session.rollback()
            raise ValueError(f"The {attribute} '{value}' provided exists") from e
        else:
            session.rollback()
            raise ValueError("Duplicate entry detected") from e


def populate_dates(session, DateModel, start_date=None, years_ahead=2):
    """
    Populates the dates table for the next `years_ahead` years from the given
        `start_date`.
    If no start_date is provided, uses today's date.

    Args:
        session (obj): The current db session
        DateModel (cls): The class `Date` defined in models
        Start_date (obj): The date object to start populating.
                          defaults to today()
        years_ahead (int): number of years on which the database is to be
                           populated.
                           defaults to 10 years.
    """
    from datetime import datetime, timedelta

    if start_date is None:
        start_date = datetime.today().date()

    # Calculate the end date (n years from start_date)
    end_date = start_date + timedelta(days=years_ahead * 365)

    current_date = start_date

    while current_date <= end_date:
        try:
            """check if date already exists"""
            existing_date = session.query(DateModel).filter_by(
                                          date=current_date).first()
            if not existing_date:
                new_date = DateModel(date=current_date)
                session.add(new_date)
            current_date += timedelta(days=1)
            session.commit()
        except IntegrityError:
            session.rollback()

    # print(f"Dates populated up to {end_date}")


def ensure_future_dates(session, DateModel):
    """
    Ensures the dates table has at least one year of future dates populated.
    """
    import datetime
    # Get the latest date in the dates table
    latest_date = session.query(DateModel.date).order_by(DateModel.date.desc()).first()

    if latest_date:
        latest_date = latest_date[0]  # Extract the date
    else:
        # If no dates exist, start from today
        latest_date = datetime.today().date()

    # Check if the difference is less than 1 year
    if (latest_date - datetime.today().date()).days < 365:
        populate_dates(start_date=latest_date + datetime.timedelta(days=1))


def populate_time_table(session, TimeModel):
    """
    Populates the time table with all combinations of
    hours and minutes (00:00 to 23:59).
    """
    # from datetime import time

    for hour in range(24):  # 00 to 23
        for minute in range(60):  # 00 to 59
            from datetime import time
            new_time = time(hour, minute)

            # Check if the time already exists in the database
            if not session.query(TimeModel).filter_by(saa=new_time).first():
                new_time_record = TimeModel(hour=hour, minute=minute)
                session.add(new_time_record)

    session.commit()
    # print("Time table populated successfully.")
