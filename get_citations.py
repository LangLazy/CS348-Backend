from db import database

def find_citations(root_ID):
    db = database()
    query = '''
                Select p.paper_id, p.title, p.n_citation
                From (with recursive 
                        HasCited(paper_id, cites_paper_id) AS 
                            ((SELECT paper_id, cites_paper_id FROM citations WHERE paper_id = %s)
                            UNION
                            (SELECT citations.paper_id, citations.cites_paper_id
                                FROM HasCited HC, citations
                                WHERE HC.cites_paper_id = citations.paper_id
                            ))
                        SELECT cites_paper_id
                        FROM HasCited
                    ) as t, paper as p
                WHERE t.paper_id = p.paper_id
            '''
    result = db.execute(query, [root_ID])
    return result