from src.mathe import multiply

def test_basic_math():
    assert 4+4==8

def test_multiply():
    assert multiply (3, 5) == 15

def multiple_negative():
    assert multiply(-3, 5) == -15