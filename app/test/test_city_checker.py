from utils.city_checker import city_checker


def test_city_checker_with_str():
    str_input = "los angeles"
    assert city_checker(str_input) == True


def test_city_checker_with_long_str():
    str_input = "los angeles york florida vegas seattle rio athens"
    assert city_checker(str_input) == True
