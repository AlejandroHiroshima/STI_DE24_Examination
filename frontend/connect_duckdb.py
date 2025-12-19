import duckdb
from pathlib import Path
import pandas as pd

db_path = Path(__file__).parents[1] / "strength.duckdb"

def query_strength_duckdb(athlete_name: str, start_date: str, end_date: str) -> pd.DataFrame :
    with duckdb.connect(str(db_path), read_only=True) as conn:
        query=(f"""
            SELECT 
                *
            FROM
                main_mart.mart_strength
            WHERE
                LOWER(athlete_first_name) = LOWER(?)
            AND
                full_workout_date BETWEEN ? AND ?
            AND 
                exercise_name IS NOT NULL;    
""")    
        result = conn.execute(query, [athlete_name, start_date, end_date] )    
        return result.df()
    
# if __name__ == "__main__":
    # Test med riktiga värden
    # df = query_strength_duckdb("Erik", "2025-01-01", "2025-10-25")
    
    # print(f"Rows fetched: {len(df)}")
    # print(f"\nColumns: {df.columns.tolist()}")
    
    # if len(df) > 0:
    #     print(f"\nFirst 5 rows:")
    #     print(df.head())
    #     print(f"\nData types:")
    #     print(df.dtypes)
    # else:
    #     print("\n⚠️ No data found! Check:")
    #     print("  - Database path:", db_path)
    #     print("  - Athlete name spelling")
    #     print("  - Date range")
    # print(f"Looking for DB at: {db_path}")
    # print(f"DB exists: {db_path.exists()}")   
    
def query_cardio_duckdb(athlete_name: str, start_date: str, end_date: str) -> pd.DataFrame :
    with duckdb.connect(str(db_path), read_only=True) as conn:
        query=(f"""
            SELECT 
                *
            FROM
                main_mart.mart_cardio
            WHERE
                full_workout_date BETWEEN ? AND ?;    
""")    
        result = conn.execute(query, [athlete_name, start_date, end_date] )    
        return result.df() 

if __name__ == "__main__":
    with duckdb.connect(str(db_path), read_only=True) as conn:
     print(conn.execute("""
                SELECT 
                *
                FROM main_mart.mart_cardio
            """).df())