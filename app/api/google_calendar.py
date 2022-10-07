from pprint import pprint

from api.Google import Create_Service, convert_to_RFC_datetime
from api.google_apis import *


CLIENT_SECRET_FILE = "client_secret_google_calendar.json"
API_NAME = "calendar"
API_VERSION = "v3"

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.events.readonly",
]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
calendar_id_kevin_primary = "kevinzy17@gmail.com"

"""
Create a Calendar Event
"""


def create_google_calendar_event(
    start_year_input: int,
    start_month_input: int,
    start_day_input: int,
    start_hour_input: int,
    start_minute_input: int,
    end_year_input: int,
    end_month_input: int,
    end_day_input: int,
    end_hour_input: int,
    end_minute_input: int,
    event_title_input: str,
    description_input: str,
    location_input: str,
):
    int_start_year_input = int(start_year_input)
    int_start_month_input = int(start_month_input)
    int_start_day_input = int(start_day_input)
    int_start_hour_input = int(start_hour_input)
    int_start_minute_input = int(start_minute_input)
    int_end_year_input = int(end_year_input)
    int_end_month_input = int(end_month_input)
    int_end_day_input = int(end_day_input)
    int_end_hour_input = int(end_hour_input)
    int_end_minute_input = int(end_minute_input)

    if not description_input:
        description_input = ""

    if not location_input:
        location_input = ""

    event_request_body = {
        "start": {
            "dateTime": convert_to_RFC_datetime(
                int_start_year_input,
                int_start_month_input,
                int_start_day_input,
                int_start_hour_input,
                int_start_minute_input,
            ),
            # "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": convert_to_RFC_datetime(
                int_end_year_input,
                int_end_month_input,
                int_end_day_input,
                int_end_hour_input,
                int_end_minute_input,
            ),
            # "timeZone": "America/Los_Angeles",
        },
        "summary": str(event_title_input),
        "description": str(description_input),
        "colorId": 9,
        "status": "confirmed",
        "transparency": "opaque",
        "visibility": "private",
        "location": str(location_input),
    }

    sendNotifications = True
    sendUpdates = "all"
    supportsAttachments = True

    response = (
        service.events()
        .insert(
            calendarId=calendar_id_kevin_primary,
            sendNotifications=sendNotifications,
            sendUpdates=sendUpdates,
            supportsAttachments=supportsAttachments,
            body=event_request_body,
        )
        .execute()
    )

    print(
        "Jarvis successfully created a Google Calendar event. Here are the details:\n"
    )
    pprint(response)
