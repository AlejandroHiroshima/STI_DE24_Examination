import duckdb
from constants import DUCKDB_PATH

def connect_duckdb(sql_code: str, parameters=None):
    with duckdb.connect(DUCKDB_PATH) as conn:
        
        connection = conn.execute(sql_code, parameters)
        
        return connection.df()
    
    
df = connect_duckdb("desc;")
print(df.head())
    
    

        
    

