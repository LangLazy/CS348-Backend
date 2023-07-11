from db import database

def generate_query(paperid, **kwargs):
    if len(kwargs) == 0:
        return
    query = ["UPDATE paper", "SET"]
    pieces = []
    args = []
    for k,v in kwargs.items():
        pieces.append(f"{k} = %s")
        args.append(v)
    query.append(' , '.join(pieces))
    query.append("WHERE paper_id = %s")
    full = (" ".join(query))
    print(full)
    args.append(paperid)
    return (full,args)

def update_paper(paperid, **kwargs):
    db = database()
    query, args = generate_query(paperid, **kwargs)
    db.execute(query, args, False)