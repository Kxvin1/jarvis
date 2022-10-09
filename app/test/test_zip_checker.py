from utils.zip_checker import zip_checker


def test_zip_checker_str():
    zip_input = "90210"
    assert zip_checker(zip_input) == True


def test_zip_checker_str_2():
    zip_input_2 = "33162"
    assert zip_checker(zip_input_2) == True
