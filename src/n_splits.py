def n_splits(l, n):
    """
    I'm too lazy to get this to split in an interesting way for small
    size of l, small n. Some n's will not produce unique splits of l
    for small sizes of l.

    There's an extra +1 floating around the index splits because I 
    would rather have oddly large splits than have an extra tiny last split.
    """
    ls = [l[i*int(1 + (len(l)/n)):(1 + i)*int(1 + (len(l)/n))] for i in range(n)]
    last_split = l[n*int(1 + (len(l)/n)):]
    if len(last_split) and (not last_split in ls):
        ls.append(last_split)
    return ls