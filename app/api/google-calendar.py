from pprint import pprint
from Google import Create_Service


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

print(dir(service))
