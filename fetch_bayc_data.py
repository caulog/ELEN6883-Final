import requests
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# ------------------ GraphQL Setup ------------------
GRAPHQL_URL = "https://api.studio.thegraph.com/query/110146/bayc-holdtime/version/latest"
query = """
{
  transfers(first: 1000, orderBy: blockTimestamp, orderDirection: asc) {
    tokenId
    from
    to
    blockTimestamp
    transactionHash
  }
}
"""
response = requests.post(GRAPHQL_URL, json={"query": query})
transfers = response.json()["data"]["transfers"]
df = pd.DataFrame(transfers)
df["blockTimestamp"] = pd.to_datetime(pd.to_numeric(df["blockTimestamp"]), unit="s")

# ------------------ Google Sheets Setup ------------------
# Set up Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("../bayc-holdtime-data-7a41b271118d.json", scope)
client = gspread.authorize(creds)

# Open or create a Google Sheet
sheet = client.open("bayc-holdtime-data").sheet1  # must be shared with your service account

# Write DataFrame to sheet
set_with_dataframe(sheet, df)

print("Data exported to Google Sheets!")

