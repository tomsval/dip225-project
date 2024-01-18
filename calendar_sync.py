import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import ics


class CalendarSync:
    def __init__(self):
        self.SCOPES = ["https://www.googleapis.com/auth/calendar"]
        self.build_api_service("credentials.json")

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
            print("Pabeigts!")

        except HttpError as err:
            print(f"Kļūda: {err}")

    def ics_to_google_calendar_format(self) -> list:
        with open("grafiks.ics") as f:
            ical = ics.Calendar(f.read())

        gevent_list = []
        for event in ical.events:
            gevent = {
                "summary": event.name,
                "start": {"dateTime": event.begin.isoformat()},
                "end": {"dateTime": event.end.isoformat()},
                "location": event.location,
                "reminders": {"useDefault": True},
            }

            gevent_list.append(gevent)

        return gevent_list

    def sync_calendar(self):
        event_list = self.ics_to_google_calendar_format()
        print(event_list[0]["summary"])

        base_calendar = {
            "summary": str(datetime.datetime.now()),
            "timeZone": "Europe/Riga",
        }

        ortus_calendar = self.service.calendars().insert(body=base_calendar).execute()

        print(f"Kalendārs izveidots: {ortus_calendar['id']}")

        for event in event_list:
            print(event)
            google_event = (
                self.service.events()
                .insert(calendarId=ortus_calendar["id"], body=event)
                .execute()
            )
            print(f"Notikums pievienots: {google_event.get("htmlLink")}")
