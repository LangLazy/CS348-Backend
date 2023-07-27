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
            SELECT Distinct HasCited.paper_id, HasCited.cites_paper_id, p.title, p.n_citation
            FROM HasCited LEFT OUTER JOIN paper as p
            ON HasCited.cites_paper_id = p.paper_id
            '''
    result = db.execute(query, [root_ID])
    return result