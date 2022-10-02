from datetime import datetime


def get_current_time():
    now = datetime.now()
    current_time_12 = now.strftime("%m/%d/%Y %I:%M:%S %p")
    return current_time_12
