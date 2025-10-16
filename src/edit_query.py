def edit_query(query_file, r_lines):
    """
    Contain the lines to be replaced in the query by
    # begin moving parameter lines 
    ...
    # end moving parameter lines
    including the octothorpes.
    """

    q = ""
    with open(query_file, 'r') as f:
        for line in f:
            q += f.read()

    q_lines = q.splitlines()

    i = 1
    if len(r_lines):
        for new_line in r_lines:
            q_lines[q_lines.index('# begin moving parameter lines') + i] = new_line
            i += 1
    else:
        return q
    
    new_q = '\n'.join(q_lines)

    return new_q

