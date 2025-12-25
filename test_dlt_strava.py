import os
from datetime import datetime, timezone

import dlt
from dotenv import load_dotenv

from backend.load_strava_data import strava_source

load_dotenv()

if __name__ == "__main__":
    print("DUCKDB_PATH:", os.getenv("DUCKDB_PATH"))
    print("STRAVA_CLIENT_ID:", os.getenv("STRAVA_CLIENT_ID"))
    print("STRAVA_REFRESH_TOKEN prefix:", os.getenv("STRAVA_REFRESH_TOKEN")[:6] + "...")

    pipeline = dlt.pipeline(
        pipeline_name="test_strava_pipeline",
        destination="duckdb",   # ingen credentials här
        dataset_name="staging",
    )

    source = strava_source()

    load_info = pipeline.run(source)

    print("=== DLT LOAD INFO ===")
    print(load_info)
    if pipeline.last_trace and pipeline.last_trace.last_normalize_info:
        print("Row counts:", pipeline.last_trace.last_normalize_info.row_counts)
    else:
        print("No normalize info (troligen 0 rader)")