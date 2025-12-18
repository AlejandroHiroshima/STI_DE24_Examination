import duckdb
from pathlib import Path

# DUCKB_PATH = Path(__file__).parents[1] / "strength.duckdb"

def connect_duckdb(sql_code: str, parameters=None):
    with duckdb.connect(Path(__file__).parents[1] / "strength.duckdb") as conn:
        
        connection = conn.execute(sql_code, parameters)
        
        return connection.df()
    
    
df = connect_duckdb("desc;")
print(df.head())

if __name__ == "__main__":
    connect_duckdb()
 
    

        
    

