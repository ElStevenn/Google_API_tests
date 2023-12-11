
# [START sheets_create]
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
import os.path
import re



class Document_CRUD():
    """
    
        *add description here explaining what exacly is this*
    
    """

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    def __init__(self,   Spreadsheet_ID = None):
        self.Spreadsheet_ID = Spreadsheet_ID
    
    def auth(self):
        creds = None
        if os.path.exists(Path("services/token.json")):
            creds = Credentials.from_authorized_user_file(Path("services/token.json"), self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    Path("services/credentials.json"), self.SCOPES
                )
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(Path("services/token.json"), "w") as token:
                    token.write(creds.to_json())
        elif creds and creds.expired and creds.refresh_token:
            # This else-if block ensures that flow is defined even if creds are expired and refreshable.
            creds.refresh(Request())
        else:
            # Define flow outside of the if-else block
            flow = InstalledAppFlow.from_client_secrets_file(
                Path("services/credentials.json"), self.SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(Path("services/token.json"), "w") as token:
                token.write(creds.to_json())

        return build("sheets", "v4", credentials=creds)

    def get_sheet_id(self, sheet_name):
        service = self.auth()
        spreadsheet_info = service.spreadsheets().get(spreadsheetId=self.Spreadsheet_ID).execute()
        for sheet in spreadsheet_info['sheets']:
            if sheet['properties']['title'] == sheet_name:
                return sheet['properties']['sheetId']
        return None  # Or handle the case where the sheet name is not found


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

    def append(self, range_name, value_input_option, values):
        try:
            service = self.auth()

            # Append data to the sheet
            body = {"values": values}
            append_result = service.spreadsheets().values().append(
                spreadsheetId=self.Spreadsheet_ID,
                range=range_name,
                valueInputOption=value_input_option,
                insertDataOption="INSERT_ROWS",
                body=body
            ).execute()

            # Calculate the new row indices for borders
            updated_range = append_result.get('updates', {}).get('updatedRange', '')
            start_row_index = self.extract_row_index(updated_range)
            num_rows = append_result.get('updates', {}).get('updatedRows', 0)
            end_row_index = start_row_index + num_rows

            # Assuming you have a valid method to get the sheet ID
            sheet_id = self.get_sheet_id("Your Sheet Name")  # Replace "Your Sheet Name" with the actual sheet name

            # Define border styles
            border_style = {
                "style": "SOLID",
                "width": 1,
                "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1}
            }

            # Border request
            border_requests = {
                "requests": [{
                    "updateBorders": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": start_row_index,
                            "endRowIndex": end_row_index,
                            "startColumnIndex": 2,  # Adjust if needed
                            "endColumnIndex": 7     # Adjust if needed
                        },
                        "top": border_style,
                        "bottom": border_style,
                        "left": border_style,
                        "right": border_style,
                        "innerHorizontal": border_style,
                        "innerVertical": border_style
                    }
                }]
            }

            # Update borders
            service.spreadsheets().batchUpdate(
                spreadsheetId=self.Spreadsheet_ID, 
                body=border_requests
            ).execute()

            return append_result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
    
    def extract_row_index(self, range_string):
        # Pattern to match the row number in the range string (e.g., '5' in 'Sheet1!A5:Z5')
        match = re.search(r'(\d+)', range_string.split('!')[1])
        if match:
            return int(match.group(1)) - 1  # Subtract 1 to convert to zero-based index
        else:
            return 0  # Default to 0 if no match is found
        
if __name__ == "__main__":
    sheet = Document_CRUD()
    sheet.Spreadsheet_ID = "1kpj7e08JrhsH4WKJhQeIYXWUh4k4Nc4vKSd-DuZqpVw"
    valueInputOption = "USER_ENTERED"
    range_name = "C9:G9"
    values = [["Pepe","García","19","pepardogarcia@gmail.com","+34 640523319"]]


    sheet.append(range_name, valueInputOption, values)