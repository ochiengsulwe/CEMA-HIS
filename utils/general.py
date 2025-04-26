"""The module contains helper methods to routes which don't need require the
application instance to interact with the database.
"""
from flask import jsonify


def verify_data(data, fields):
    """Makes sure only needed data is pushed to database.

         It will delete any unrequired fiels present from the JSON payload.
         Args:
            data(dict): The serialised json data received from user.
            fields(list of str): a list of expected attributes.
    """
    keys_to_delete = [key for key in data if key not in fields]

    for key in keys_to_delete:
        del data[key]


def data_check(data, fields):
    """Validates if the route has received all required fields.

        Args:
            data(dict): key/value pair of values to be received.
            fields(list of str): a list of expected attributes.

        Returns:
            abort: aborts with error 400.
            On success, does nothing.

    """
    verify_data(data, fields)
    for item in fields:
        if item not in data:
            return jsonify({'error': f'{item} is needed'}), 400
