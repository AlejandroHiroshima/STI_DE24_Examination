import io # io ???
import requests
import pandas as pd
import dlt
import duckdb
from constants import DUCKDB_PATH, CSV_URL_ALEX, CSV_URL_ERIK

@dlt.resource(name="historical_strength_data_alex", write_disposition = "replace", table_name="stg_alex",)
def fetch_alex_strength_data():
    data = requests.get(CSV_URL_ALEX, timeout=30)
    data.raise_for_status()
    df= pd.read_csv(io.StringIO(data.text))
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    for rec in df.to_dict(orient = "records"): 
        yield rec


@dlt.resource(name="historical_strength_data_erik", write_disposition = "replace", table_name="stg_erik",)
def fetch_erik_strength_data():
    data = requests.get(CSV_URL_ERIK, timeout=30)
    data.raise_for_status()
    df= pd.read_csv(io.StringIO(data.text))
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    for rec in df.to_dict(orient = "records"): 
        yield rec

pipeline = dlt.pipeline(
    pipeline_name="strengthlog_google_sheet_to_duckdb",
    destination= dlt.destinations.duckdb(DUCKDB_PATH),
    dataset_name="staging",
)

if __name__ == '__main__':
    load_info = pipeline.run(fetch_alex_strength_data)
    load_info = pipeline.run(fetch_erik_strength_data)

    print(load_info) 