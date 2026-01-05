import io
import requests
import pandas as pd
import dlt
from .constants import DUCKDB_PATH, CSV_URL_ALEX, CSV_URL_ERIK

fix_columns = ["weight_kg", "athlete_weight_kg", "extra_weight_kg", "total_volume_session"] # "athlete_weight_kg"

@dlt.resource(name="historical_strength_data_alex", write_disposition = "replace", table_name="stg_alex",)
def fetch_alex_strength_data():
    data = requests.get(CSV_URL_ALEX, timeout=30)
    data.raise_for_status()
    df= pd.read_csv(io.StringIO(data.text))
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    for c in df.columns:
        if c in fix_columns:
            df[c] = df[c].str.replace(',','.')
    for rec in df.to_dict(orient = "records"): 
        yield rec


@dlt.resource(name="historical_strength_data_erik", write_disposition = "replace", table_name="stg_erik",)
def fetch_erik_strength_data():
    data = requests.get(CSV_URL_ERIK, timeout=30)
    data.raise_for_status()
    df= pd.read_csv(io.StringIO(data.text))
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    for c in df.columns:
        if c in fix_columns:
            df[c] = df[c].str.replace(',','.')
    for rec in df.to_dict(orient = "records"): 
        yield rec

pipeline = dlt.pipeline(
    pipeline_name="strengthlog_google_sheet_to_duckdb",
    destination= dlt.destinations.duckdb(DUCKDB_PATH),
    dataset_name="staging",
)

@dlt.source
def strength_source():
    return [fetch_alex_strength_data(), fetch_erik_strength_data()]

if __name__ == '__main__':
    load_info = pipeline.run(strength_source())
    print(load_info) 