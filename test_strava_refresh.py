import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN_URL = "https://www.strava.com/oauth/token"
BASE_URL = "https://www.strava.com/api/v3"


def refresh():
    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")
    refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")

    print("CLIENT_ID:", client_id)
    print("REFRESH_TOKEN (bör EJ vara tom):", refresh_token[:6] + "..." if refresh_token else None)

    resp = requests.post(
        TOKEN_URL,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=30,
    )
    print("refresh status:", resp.status_code, resp.text)
    resp.raise_for_status()
    data = resp.json()
    access_token = data["access_token"]
    print("NEW ACCESS TOKEN:", access_token[:10], "...")
    return access_token


def test_activities(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"per_page": 1, "page": 1}
    resp = requests.get(f"{BASE_URL}/athlete/activities", headers=headers, params=params, timeout=30)
    print("activities status:", resp.status_code, resp.text[:200])
    resp.raise_for_status()


if __name__ == "__main__":
    token = refresh()
    test_activities(token)