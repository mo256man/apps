from google.oauth2.service_account import Credentials
import gspread

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    "mail2teams-b8254581fcbc.json",
    scopes=scopes
)

gc = gspread.authorize(credentials)

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1KXGZ89_v5OLOJfc738aVs7X4BSPy8zpIrq6mik8LrHI"

spreadsheet = gc.open_by_url(spreadsheet_url)
print(spreadsheet.sheet1.get_all_values())