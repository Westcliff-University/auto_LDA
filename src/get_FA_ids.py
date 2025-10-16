import numpy as np
import os
from dotenv import load_dotenv
import pandas as pd
import textwrap 
import pyodbc
import requests
import json
from datetime import datetime, timedelta

load_dotenv()

def create_query_string(sql_full_path: str): 
        """
        Converts a SQL query to a string. Useful for editing the string (and thus the query) itself
        to filter by flags not well defined in the database itself.

        Keyword arguments:
        sql_full_path -- string determining the file location of the query to be read in

        """
        
        with open(sql_full_path, 'r') as f_in: 
            lines = f_in.read() 
    
        # remove any common leading whitespace from every line     
        query_string = textwrap.dedent("""{}""".format(lines)) 
    
        return query_string 

def get_FA_ids(domestic: bool):
    """
    Gets the list of students from a particular Slate report to append later to a SQL query.
    Then obtains the combined list from the database and Slate.

    Keyword arguments:
    domestic -- boolean determining which SQL query to use
    """
    
    # use the basic authentication url
    # url = "https://connect.westcliff.edu/manage/query/run?id=58ccecc5-48c5-4984-8fc1-bfd8fc7b5b21&run=d682f363-de77-44c0-b6bd-3b41eae3ad2a"
    url = "https://connect.westcliff.edu/manage/query/run?id=1a0d672e-b004-4ca9-9dbc-7188e83f596b&cmd=service&output=csv&h=a0016cfc-469e-40d9-8ee7-902403b8b66e"
    #build a JSON payload
    payload = json.dumps({
    "row": {
        "fieldKey": "fieldData"
    }
    })

    # add headers
    headers = {
    'Authorization': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ=',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(str(response.status_code) + ": " + response.text)

    f = open('slate_data.csv','w')
    f.write(response.text) #Give your csv text here.
    ## Python will convert \n to os.linesep
    f.close()

    df = pd.read_csv('slate_data.csv')

    id_string = ""
    for sid in df['sis_studentidentifier'].unique():
        id_string += "\'" + str(sid) + "\',"

    last_sql_line = "OR MAX(p.StudentIdentifier) IN (" + id_string[:-1] + ")"

    if domestic:
        path = "LDA_info.sql"
    else:
        path = "DGE_LDA_info.sql"
    query = create_query_string(path)
    cnxn = pyodbc.connect(os.environ.get('S1_CONN_STR'))

    crsr = cnxn.cursor()

    query += last_sql_line
    query += " ORDER BY MAX(s.StartDate) DESC"

    sis_df = pd.read_sql(query,cnxn)
    if domestic:
        sis_df.to_csv('../data/sis_dump.csv', index = False)
    else:
        sis_df.to_csv('../data/DGE_sis_dump.csv', index = False)
    crsr.close()
    cnxn.close()

    ids = list(sis_df['StudentAssignedID'].unique())

    return ids

# print("COPY AND PASTE THESE INTO THE REPORTS LISTED ABOVE")
#AND c.fullname NOT IN ('Westcliff_Library')
#AND c.fullname NOT LIKE '%Orientation%'
#AND c.fullname NOT LIKE '%NSO%'