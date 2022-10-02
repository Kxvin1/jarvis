import re


def zip_checker(zip_code):
    if re.search(r"^\d{5}$", zip_code, re.IGNORECASE):
        return True
    return False
