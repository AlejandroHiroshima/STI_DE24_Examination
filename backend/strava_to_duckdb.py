# strava_to_duckdb.py
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import dlt
from constants import DUCKDB_PATH

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

def refresh_access_token():
    """Refresh the Strava access token using the refresh token."""
    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    
    response = requests.post(url, data=payload)
    response.raise_for_status()
    
    data = response.json()
    new_access_token = data["access_token"]
    new_refresh_token = data["refresh_token"]
    
    with open(".env", "r") as f:
        lines = f.readlines()
    
    with open(".env", "w") as f:
        for line in lines:
            if line.startswith("STRAVA_ACCESS_TOKEN="):
                f.write(f"STRAVA_ACCESS_TOKEN={new_access_token}\n")
            elif line.startswith("STRAVA_REFRESH_TOKEN="):
                f.write(f"STRAVA_REFRESH_TOKEN={new_refresh_token}\n")
            else:
                f.write(line)
    
    print("✅ Access token refreshed successfully")
    return new_access_token

def fetch_strava_activities(access_token, after_date, before_date):
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    after_timestamp = int(after_date.timestamp())
    before_timestamp = int(before_date.timestamp())
    
    params = {
        "after": after_timestamp,
        "before": before_timestamp,
        "per_page": 200 
    }
    
    all_activities = []
    page = 1
    
    while True:
        params["page"] = page
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        activities = response.json()
        
        if not activities:
            break
        
        all_activities.extend(activities)
        page += 1
    
    print(f"✅ Fetched {len(all_activities)} activities from Strava")
    return all_activities

def load_to_duckdb(activities):
    """Load activities into DuckDB using dlt with merge strategy."""
    
    @dlt.resource(name="strava_activities", write_disposition="replace", table_name = "staging_cardio")
    def strava_activities_resource():
        yield activities
    
    pipeline = dlt.pipeline(
        pipeline_name="strava_pipeline",
        destination=dlt.destinations.duckdb(DUCKDB_PATH),
        dataset_name="staging"
    )
    
    load_info = pipeline.run(strava_activities_resource())
    print(f"✅ Data loaded to DuckDB: {load_info}")

def main():
    after_date = datetime(2021, 3, 15)
    before_date = datetime.now()
    
    print(f"📅 Fetching activities from {after_date.date()} to {before_date.date()}")
    
    access_token = refresh_access_token()
    
    activities = fetch_strava_activities(access_token, after_date, before_date)
    
    if activities:
        load_to_duckdb(activities)
        print("✅ Pipeline completed successfully!")
    else:
        print("⚠️ No activities found in the specified date range")

if __name__ == "__main__":
    main()