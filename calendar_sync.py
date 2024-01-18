import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import icalendar


class CalendarSync:
    def __init__(self):
        self.SCOPES = ["https://www.googleapis.com/auth/calendar"]
        self.ics_to_google_calendar_format()
        # self.build_api_service("credentials.json")

    def build_api_service(self, credentials_path: str):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            self.service = build("calendar", "v3", credentials=creds)

            self.sync_calendar()

        except HttpError as err:
            print(f"Kļūda: {err}")

    def ics_to_google_calendar_format(self):
        with open("grafiks.ics") as f:
            ics = icalendar.Calendar.from_ical(f.read())

    def sync_calendar(self):
        pass
