# OBS SKA BARA KÖRAS EN GÅNG!
import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI")

if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]):
    raise SystemExit("Sätt STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET och STRAVA_REDIRECT_URI i .env först.")

def upsert_env_vars(new_vars: dict, env_path: str = ".env") -> None:
    """Uppdaterar/adderar nycklar i .env på ett enkelt sätt."""
    if not os.path.exists(env_path):
        # Skapa fil om den inte finns
        with open(env_path, "w") as f:
            for k, v in new_vars.items():
                f.write(f"{k}={v}\n")
        return

    with open(env_path, "r") as f:
        lines = f.readlines()

    existing_keys = {line.split("=", 1)[0] for line in lines if "=" in line}

    with open(env_path, "w") as f:
        for line in lines:
            key = line.split("=", 1)[0] if "=" in line else None
            if key in new_vars:
                f.write(f"{key}={new_vars[key]}\n")
            else:
                f.write(line)

        for k, v in new_vars.items():
            if k not in existing_keys:
                f.write(f"{k}={v}\n")

def main() -> None:
    auth_url = (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={CLIENT_ID}&"
        f"response_type=code&"
        f"redirect_uri={REDIRECT_URI}&"
        f"approval_prompt=auto&"
        f"scope=activity:read_all"
    )

    print("Öppna denna URL i din webbläsare och godkänn appen:")
    print(auth_url)
    print()
    print("Efter godkännande blir du omdirigerad till din redirect URI, t.ex.:")
    print("  http://localhost:8888/callback?code=DIN_KOD_HÄR&scope=read,activity:read_all")
    print()

    auth_code = input("Klistra in värdet efter 'code=' här: ").strip()

    token_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
    }

    resp = requests.post(token_url, data=payload)
    if not resp.ok:
        print("❌ Fel vid tokenhämtning:")
        print(resp.status_code, resp.text)
        return

    data = resp.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    upsert_env_vars(
        {
            "STRAVA_ACCESS_TOKEN": access_token,
            "STRAVA_REFRESH_TOKEN": refresh_token,
        }
    )

    print("✅ Tokens hämtade och sparade i .env")

if __name__ == "__main__":
    main()