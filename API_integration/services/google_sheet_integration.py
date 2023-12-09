
# [START sheets_create]
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path




class Document_CRUD():
    """
    
        *add description here explaining what exacly is this*
    
    """

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    def __init__(self,   Spreadsheet_ID = None):
        self.Spreadsheet_ID = Spreadsheet_ID
    
    def auth(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
        elif creds and creds.expired and creds.refresh_token:
            # This else-if block ensures that flow is defined even if creds are expired and refreshable.
            creds.refresh(Request())
        else:
            # Define flow outside of the if-else block
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", self.SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return build("sheets", "v4", credentials=creds)


    def create(self, title: str):
        try:
            service = self.auth()
            spreadsheet = {"properties": {"title": title}}
            spreadsheet = (
                service.spreadsheets()
                .create(body=spreadsheet, fields="spreadsheetId")
                .execute()
            )
            print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
            return spreadsheet.get("spreadsheetId")

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def get_values(self):
        pass

    def batch_get_values(self):
        pass


if __name__ == "__main__":
    sheet = Document_CRUD()
    sheet.create("My own math")

