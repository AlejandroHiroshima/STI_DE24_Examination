import duckdb
from pathlib import Path
import pandas as pd


# --- Ingest strength data to dashboard 
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
    
#--- Ingest Cardiodata to dashboard

def query_cardio_duckdb(activity_type: str, start_date: str, end_date: str) -> pd.DataFrame:
    with duckdb.connect(str(db_path), read_only=True) as conn:
        if activity_type == "All": # All exercise
            query = """
                SELECT *
                FROM main_mart.mart_cardio
                WHERE full_workout_date BETWEEN ? AND ?;
            """
            params = [start_date, end_date]
        else: # Selected types 
            query = """  
                SELECT *
                FROM main_mart.mart_cardio
                WHERE activity_type = ?
                  AND full_workout_date BETWEEN ? AND ?;
            """
            params = [activity_type, start_date, end_date]
        
        result = conn.execute(query, params)
        return result.df()
