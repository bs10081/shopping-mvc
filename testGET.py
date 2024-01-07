import requests
import os
from dotenv import load_dotenv

# Load .env file variables
load_dotenv()

# Environment variables
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID_PRODUCTS')

# Ensure environment variables are set
if not NOTION_API_KEY or not NOTION_DATABASE_ID:
    raise ValueError(
        "Please set the NOTION_API_KEY and NOTION_DATABASE_ID environment variables.")

# Headers for Notion API
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

# The URL for querying the database
query_database_url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"

# Send a GET request to query the database
response = requests.post(query_database_url, headers=HEADERS)

# Check the response
if response.status_code == 200:
    print("Successfully retrieved the database information from Notion.")
    # Here you would add your logic to process the response and extract the data you need
    database_info = response.json()
    print(database_info)
else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)
