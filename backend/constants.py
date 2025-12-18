from pathlib import Path

CSV_URL_ALEX = "https://docs.google.com/spreadsheets/d/1gW5Yjn3FqWePsQzxXogLH2Qvpv83bzPmZmpyzBvzrhs/gviz/tq?tqx=out:csv&sheet=Alex"
CSV_URL_ERIK = "https://docs.google.com/spreadsheets/d/1gW5Yjn3FqWePsQzxXogLH2Qvpv83bzPmZmpyzBvzrhs/gviz/tq?tqx=out:csv&sheet=Erik"
DUCKDB_PATH = Path(__file__).parents[1] / "strength.duckdb"

print(DUCKDB_PATH)