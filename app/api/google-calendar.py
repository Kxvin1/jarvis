from pprint import pprint
from Google import Create_Service, convert_to_RFC_datetime


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
calender_id_kevin_primary = "kevinzy17@gmail.com"

"""
Create a Calendar Event
"""
hour_adjustment = -8  # pacific is utc - 8

# time inputs use military 24 hour time
start_year = 2022
start_month = 12
start_day = 25
start_hour = 12 - hour_adjustment
start_minute = 30

end_year = 2022
end_month = 12
end_day = 25
end_hour = 12 - hour_adjustment
end_minute = 59

event_title_input = "event title here"
description_input = "description here"
location_input = (
    "location input here (can be a coordinate (lat/long) or city name or address)"
)

event_request_body = {
    "start": {
        "dateTime": convert_to_RFC_datetime(
            start_year, start_month, start_day, start_hour, start_minute
        ),
        "timeZone": "America/Los_Angeles",
    },
    "end": {
        "dateTime": convert_to_RFC_datetime(
            end_year, end_month, end_day, end_hour, end_minute
        ),
        "timeZone": "America/Los_Angeles",
    },
    "summary": event_title_input,
    "description": description_input,
    "colorId": 9,
    "status": "confirmed",
    "transparency": "opaque",
    "visibility": "private",
    "location": location_input,
}

sendNotifications = True
sendUpdates = "all"
supportsAttachments = True

response = (
    service.events()
    .insert(
        calendarId=calender_id_kevin_primary,
        sendNotifications=sendNotifications,
        sendUpdates=sendUpdates,
        supportsAttachments=supportsAttachments,
        body=event_request_body,
    )
    .execute()
)

pprint(response)

"""
Update a Calendar Event
"""


"""
Delete a Calendar Event
"""
