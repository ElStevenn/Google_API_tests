# [START sheets_create]
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
SAMPLE_RANGE_NAME = "Class Data!A2:E"

def create(title):
  """
  Creates the Sheet the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds = None
  if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())


 
  try:
    service = build("sheets", "v4", credentials=creds)
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
	

def get_values(spreadsheet_id, range_name):
  creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  try:
    service= build("sheets", "v4", credentials=creds)
    
    result = (
      service.spreadsheets()
      .values()
      .get(spreadsheetId=spreadsheet_id, range=range_name)
      .execute()
    ) # -> dict
    values = result.get('values', [])
    return values
    

  except HttpError as error:
    print(f"An error ocurred: {error}")
    return error


def batch_get_values(spreadsheet_id, _range_names):
  """
  read multiple rages
  """
  creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  try:
    service = build("sheets", "v4", credentials=creds)
    range_names = [
      ""
    ]
    result = (
      service.spreadsheets()
      .values()
      .batchGet(spreadsheetId=spreadsheet_id, ranges=_range_names)
      .execute()
    )

    values = result.get('valueRanges',[])
    return values

  except HttpError as error:
    print(f"An error ocurred: {error}")
    return error


def update_values(spreadsheet_id, range_name, value_input_option, _values):
  creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  """
  vasically,update a value by its cell cordinates
  """
  try:
    service = build("sheets", "v4", credentials=creds)

    body = {"values":_values}
    result = (
      service.spreadsheets()
      .values()
      .update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption=value_input_option,
        body=body,
      )
      .execute()
    )

    print(f"{result.get('updatedCells')} cells updated.")
    return result

  except HttpError as error:
    print(f"An error ocurred: {error}")
    return error

def batch_update_values(
    spreadsheet_id, range_name, value_input_option, _values
):
  """*add description here*"""
  creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  try:
    service = build("sheets", "v4", credentials=creds)
    data = [
        {"range": range_name, "values": _values},
        # Additional ranges to update ...
    ]
    body = {"valueInputOption": value_input_option, "data": data}
    result = (
        service.spreadsheets()
        .values()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
        .execute()
    )
    print(f"{(result.get('totalUpdatedCells'))} cells updated.")
    return result
  except HttpError as error:
    print(f"An error ocurred: {error}")
    return error

def append_values(spreadsheet_id, range_name, value_input_option, _values):
  """
  This is the most important doc
  """
  creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  try:
    service = build("sheets", "v4", credentials=creds)

    body = {"values": _values}

    result = (
      service.spreadsheets()
      .values()
      .append(
         spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption=value_input_option,
        body=body,
      )
      .execute()
    )
    print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
    return result

  except HttpError as error:
    print(f"An error ocurred: {error}")
    return error


if __name__ == "__main__":
  # Pass: title
  # create("pau's spreadseet")
  Spreadsheet_ID =  "1kpj7e08JrhsH4WKJhQeIYXWUh4k4Nc4vKSd-DuZqpVw"
  range_name = "A1:B1"

  append_values(Spreadsheet_ID, range_name, "USER_ENTERED", [["Pepe","Guardian"]])


