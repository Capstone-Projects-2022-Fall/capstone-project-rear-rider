from test_bluetooth import test_config_characteristic

def test_cases():
    """
    Returns all the test cases in the bluetooth module.
    """
    return [
        *test_config_characteristic.test_cases()
    ]