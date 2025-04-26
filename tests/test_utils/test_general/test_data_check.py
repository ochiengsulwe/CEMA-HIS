from utils.general import data_check


def test_data_check_success():
    """Checks when all required fields are present"""

    data = {"name": "sulwe", "age": 29}
    required_data = ["name", "age"]

    response = data_check(data, required_data)

    assert response is None


def test_a_field_missing():
    """Tests when a field is missing"""

    data = {"name": "sulwe"}
    required_data = ["name", "age"]

    response, status_code = data_check(data, required_data)

    assert status_code == 400
    assert response.get_json() == {"error": "age is needed"}
