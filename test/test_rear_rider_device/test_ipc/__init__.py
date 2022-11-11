from test_ipc import test_leds_child_proc

def test_cases():
    return [
        *test_leds_child_proc.test_cases(),
    ]