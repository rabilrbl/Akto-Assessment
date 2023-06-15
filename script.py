import os
import sys
import requests
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler

# For simplicity, we are hardcoding the GitHub URL here.
GITHUB_URL = "https://github.com/akto-api-security/pii-types/blob/master/general.json"
# We can also pass the GitHub URL as an environment variable or as a command line argument.
# GITHUB_URL = os.environ.get("GITHUB_URL") if os.environ.get("GITHUB_URL") else sys.argv[1] if len(sys.argv) > 1 else print("Please provide a GitHub URL.")

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "pii_data")
MONGO_COLLECTION_NAME = os.environ.get("MONGO_COLLECTION_NAME", "patterns")
CRON_MINUTES = os.environ.get("CRON_MINUTES", 60)

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

def fetch_data(github_url: str):
    """
    Fetches data from the given GitHub URL and updates the MongoDB collection.
    """
    response = requests.get(github_url)
    if response.ok:
        data = response.json()
        if isinstance(data, dict):
            data = [data]
        collection.delete_many({})
        collection.insert_many(data)
        print("Data fetched and updated in MongoDB.")
    else:
        print("Error fetching data from GitHub.")

def trigger(minutes=int(CRON_MINUTES), github_file_link=GITHUB_URL):
    """
    Triggers the fetch_data function every given number of minutes (default: 60 minutes).
    """
    scheduler = BlockingScheduler()

    # For a single URL, you can use the following code:
    scheduler.add_job(fetch_data, 'interval', minutes=minutes, args=[github_file_link])

    # For multiple URLs, you can use the following code:
    # GITHUB_URLS = ["https://raw.githubusercontent.com/rabilrbl/akto/master/patterns.json", "https://raw.githubusercontent.com/rabilrbl/akto2/master/patterns.json"]
    # scheduler.add_job(fetch_data, 'interval', minutes=60, args=[GITHUB_URLS])

    scheduler.start()

if __name__ == "__main__":
    trigger()
