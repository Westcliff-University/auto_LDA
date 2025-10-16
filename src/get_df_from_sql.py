import pyodbc
import pandas as pd
from create_query_string import create_query_string

def get_df_from_sql(path):
    
    query = create_query_string(path)
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=studentfirst-production-central-us.database.windows.net,1433;DATABASE=westcliff.Sis.Common.API_db;UID=westcliffreportuser;PWD=r3ad0nly!us3r16;TrustServerCertificate=Yes;Encrypt=Yes')
    crsr = cnxn.cursor()
    
    #query += last_sql_line
    
    scc = pd.read_sql(query,cnxn)
    crsr.close()
    cnxn.close()

    return scc