from pathlib import Path
import os
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DUCKDB_PATH = os.getenv("DUCKDB_PATH")
CSV_URL_ALEX = os.getenv("CSV_URL_ALEX")
CSV_URL_ERIK = os.getenv("CSV_URL_ERIK")
