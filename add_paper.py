import logging
import uuid

from db import database

def publish_paper(author_id, title, year, fos_name, n_citation, url, page_start, page_end, 
                                doc_type, lang, vol, issue, issn, isbn, doi, abstract):
    logging.basicConfig(level=logging.DEBUG, force=True)
    logging.getLogger(__name__).setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)
    try:
        db = database()
        paper_id = uuid.uuid4().hex

        query = "Select * from author where author_id = %s"
        result = db.execute((query), [author_id])
        if result == []:
            return "ERROR: No such author exists"

        query = '''Insert into paper(paper_id, title, year, fos_name, n_citation, page_start, page_end, doc_type, lang, vol, issue, issn, isbn, doi, url, abstract)
                               VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        db.execute((query), [paper_id, title, year, fos_name, n_citation, page_start, page_end, 
                                doc_type, lang, vol, issue, issn, isbn, doi, url, abstract], False)

        query = "Insert into wrote(author_id, paper_id) VALUES(%s, %s)"
        db.execute((query), [author_id, paper_id], False)

        return "success"

    except Exception as e:
        log.error("I have failed brother")
        log.debug(e)
        return None