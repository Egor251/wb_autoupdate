import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import googleapiclient.discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account

import config


class DataGathering:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    CREDENTIALS_FILE = 'token.json'  # Имя файла с закрытым ключом, вы должны подставить свое

    SAMPLE_SPREADSHEET_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
    SAMPLE_RANGE_NAME = f"{config.table1_name}!A2:C"
    SAMPLE_RANGE_NAME2 = f"{config.table2_name}!A2:C"

    goods_table = config.spreadsheet_id

    def get_credentials(self):
        with open(self.CREDENTIALS_FILE, 'r') as key_file:
            key_info = json.load(key_file)
        credentials = service_account.Credentials.from_service_account_info(
            key_info,
            scopes=self.SCOPES,
        )
        return credentials

    def auth_google(self):  # Авторизация в google
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
        return creds

    def get_service_sacc(self, credentials):
        return googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)

    def get_data(self, range):
        # Call the Sheets API
        credentials = self.auth_google()
        service = self.get_service_sacc(credentials)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=self.goods_table, range=range)
            .execute()
            )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return
        return values

    def main_parse(self):
        table1 = self.get_data(self.SAMPLE_RANGE_NAME)
        table2 = self.get_data(self.SAMPLE_RANGE_NAME2)
        return table1, table2


if __name__ == '__main__':
    DataGathering().main_parse()
