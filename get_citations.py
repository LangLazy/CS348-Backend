from db import database

def find_citations(root_ID):
    db = database()
    query = '''
            with recursive 
            HasCited(paper_id, cites_paper_id) AS 
            ((SELECT paper_id, cites_paper_id FROM citations WHERE paper_id = %s)
                UNION
            (SELECT citations.paper_id, citations.cites_paper_id
            FROM HasCited HC, citations
            WHERE HC.cites_paper_id = citations.paper_id
            ))
            SELECT Distinct x.paper_id, x.cites_paper_id, x.title as cited_title, c.title
            FROM (
                SELECT HasCited.paper_id, HasCited.cites_paper_id, p.title 
                FROM HasCited LEFT OUTER JOIN paper as p
                ON HasCited.cites_paper_id = p.paper_id
            ) x
            LEFT OUTER JOIN paper c
            ON x.paper_id = c.paper_id
            '''
    result = db.execute(query, [root_ID])
    return result