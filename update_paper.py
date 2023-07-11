from db import database

def generate_query(paperid, **kwargs):
    if len(kwargs) == 0:
        return
    query = ["UPDATE paper", "SET"]
    pieces = []
    for k,v in kwargs.items():
        pieces.append(f"{k} = {v}")
    query.append(' , '.join(pieces))
    query.append("WHERE paper_id = %s")
    return (" ".join(query))

    

def update_paper(paperid, **kwargs):
    db = database()
    query = generate_query(paperid, kwargs)
    db.execute(query, [paperid], False)