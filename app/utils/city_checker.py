import re


def city_checker(city_name):
    if re.search(
        r"^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$",
        city_name,
        re.IGNORECASE,
    ):
        return True
    return False
