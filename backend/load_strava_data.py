# backend/load_strava_data.py
import os
from datetime import datetime, timezone

import dlt
import requests
from dotenv import load_dotenv

# Läs .env när modulen laddas
load_dotenv()

BASE_URL = "https://www.strava.com/api/v3"
TOKEN_URL = "https://www.strava.com/oauth/token"


def _refresh_strava_access_token() -> str:
    """
    Samma logik som i test_strava_refresh.py, men utan print av full token.
    """
    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")
    refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")

    print("[Strava] CLIENT_ID:", client_id, flush=True)
    print(
        "[Strava] REFRESH_TOKEN prefix:",
        (refresh_token[:6] + "...") if refresh_token else None,
        flush=True,
    )

    if not all([client_id, client_secret, refresh_token]):
        raise RuntimeError(
            "STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET eller STRAVA_REFRESH_TOKEN saknas i .env"
        )

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
    print("[Strava] refresh status:", resp.status_code, flush=True)
    resp.raise_for_status()
    data = resp.json()
    access_token = data["access_token"]
    print("[Strava] NEW ACCESS TOKEN prefix:", access_token[:10], "...", flush=True)

    # Uppdatera i den här processen
    os.environ["STRAVA_ACCESS_TOKEN"] = access_token
    return access_token


def _get_strava_access_token() -> str:
    """
    Hämta access token; refresha alltid inför varje körning för enkelhetens skull.
    (Detta garanterar att Dagster alltid använder en färsk token.)
    """
    print("[Strava] _get_strava_access_token: refreshing token...", flush=True)
    return _refresh_strava_access_token()


def fetch_strava_activities_raw(after: datetime, before: datetime):
    """
    Generator som hämtar aktiviteter från Strava-API:t mellan två tider.
    """
    access_token = _get_strava_access_token()
    print("[Strava] initial access_token prefix:", access_token[:10], "...", flush=True)

    headers = {"Authorization": f"Bearer {access_token}"}

    page = 1
    per_page = 200

    while True:
        params = {
            "after": int(after.timestamp()),
            "before": int(before.timestamp()),
            "page": page,
            "per_page": per_page,
        }
        print(f"[Strava] Request page={page}, params={params}", flush=True)
        resp = requests.get(
            f"{BASE_URL}/athlete/activities",
            headers=headers,
            params=params,
            timeout=30,
        )

        print("[Strava] response status:", resp.status_code, flush=True)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            print("[Strava] no more activities, done.", flush=True)
            break

        for activity in batch:
            yield activity

        page += 1


@dlt.resource(
    name="historical_strava_activities",
    write_disposition="merge",
    primary_key="id",
    table_name="staging_cardio",
)
def fetch_strava_activities():
    """
    dlt-resource som yieldar Strava-aktiviteter som dict-records.
    Dessa kommer skrivas till staging.stg_strava_activities i DuckDB.
    """
    # Samma tidsfönster som tidigare: från 2025-11-01 till nu (UTC)
    after = datetime(2025, 11, 1, tzinfo=timezone.utc)
    before = datetime.now(timezone.utc)

    for rec in fetch_strava_activities_raw(after, before):
        yield rec


@dlt.source
def strava_source():
    """
    dlt-source som samlar alla Strava-resurser (just nu bara en).
    Dagster använder den här i @dlt_assets.
    """
    return [fetch_strava_activities()]