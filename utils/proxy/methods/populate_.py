"""
This module populates a model class Table.

Same as `populate_from_date` with the difference of not dealing with datetime objects.
"""


def populate_from_data_(model_class, data_list, session):
    for data in data_list:
        instance = model_class()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        try:
            session.add(instance)
        except Exception as e:
            print(f"Error adding {data['name'] if 'name' in data else 'unknown'}: {e}")
            session.rollback()
            continue
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error committing session: {e}")
