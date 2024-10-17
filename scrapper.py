import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# loading env vars
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_SPREADSHEET_ID = str(os.getenv("SPREADSHEET_ID"))

def fetchRows(fromCol, toCol):

    # constants for the spreadsheet
    SAMPLE_RANGE_NAME = f"Sheet1!{fromCol}:{toCol}"

    creds = None

    # checking if token exists so login process could be skipped
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # if creds have expired, login again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "creds.json", SCOPES
            )

            creds = flow.run_local_server(port=0)

        # saving token for future use
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        return values

    except HttpError as err:
        print(err)

"""
NOTE: 

I just like to add comments for my own readability and debugging,
it's not GPT code :)
"""
