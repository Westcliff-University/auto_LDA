import textwrap

def create_query_string(sql_full_path): 
    with open(sql_full_path, 'r') as f_in: 
        lines = f_in.read() 
 
    # remove any common leading whitespace from every line     
    query_string = textwrap.dedent("""{}""".format(lines)) 
 
    return query_string 