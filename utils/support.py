"""
This module describes methods supporting service clarity
"""


def is_parent(child, parent):
    """
    Confirms if the parent exists as a parent to the child

    Args:
        child (obj): An object of type ChildProfile
        parent (obj): An object of type LogInfo

    Returns:
        bool: Returns True or False
    """

    if parent.adult_profile in child.parents:
        return True
    else:
        return False


def week_of_month(date_obj):
    first_day = date_obj.replace(day=1)
    dom = date_obj.day
    adjusted_dom = dom + first_day.weekday()
    return int((adjusted_dom - 1) / 7) + 1
