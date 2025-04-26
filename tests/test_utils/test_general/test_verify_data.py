from utils.general import verify_data


def test_verify_data_removes_extra_fields():
    """Tests that extra/unwaned keys are removed from parsed data"""

    data = {"name": "sulwe", "age": 29, "extra": "remove"}
    fields = ["name", "age"]

    verify_data(data, fields)

    assert data == {"name": "sulwe", "age": 29}


def test_verify_data_keeps_valid_keys():
    """Tests that valid keys should remain intact at they are entered"""

    data = {"name": "sulwe", "age": 29}
    fields = ["name", "age"]

    verify_data(data, fields)

    assert data == {"name": "sulwe", "age": 29}


def test_verify_data_empty_data():
    """Tests that empty data should always remain empty"""
    data = {}
    fields = ["name", "age"]

    verify_data(data, fields)

    assert data == {}


def test_verify_data_no_fields():
    """Tests that when no fileds are required, parsed data should be emptied"""
    data = {"null": "to remove", "void": "get it out"}
    fields = []

    verify_data(data, fields)

    assert data == {}


def test_verify_data_no_modification_of_fields():
    """Tests that no field value or key is modified/changed when matching"""
    data = {"name": "sulwe"}
    fields = ["name"]

    verify_data(data, fields)

    assert data == {"name": "sulwe"}
