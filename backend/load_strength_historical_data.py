import io # io ???
import requests
import pandas as pd
import dlt

CSV_URL = " " # google sheets URL

@dlt_resource(name="historical_strength_data", write_disposition = "replace")
def fetch_historical_strength_data():
    data = requests.get(CSV_URL, timeout=30) # timeout ???
    data.raise_for_status()
    df= pd.read_csv(io.StringIO(data.text))
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    date_cols = [c for c in df.columns if "workout_date" in c]
    for c in date_cols:
        df[c] = pd.to_datetime(df[c], errors = "coerce") 

    for rec in df.to_dict(orient = "records"): # orient?
        yield rec
pipeline = dlt.pipeline(
    pipeline_name="strengthlog_google_sheet_to_redshift",
    destination= "redshift"
)

if __name__ == '__main__':
    load_info = pipeline.run(fetch_historical_strength_data, table_name= "strength_staging") # table_name = schema?
    print(load_info)