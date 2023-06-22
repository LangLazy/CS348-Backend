from flask import Flask, request
from flask_cors import CORS, cross_origin
import hashlib

from query_keywords import query_keywords
from create_user import insert_user
from add_paper import publish_paper

app = Flask(__name__)
cors = CORS(app)

@app.route("/keywords/<keywords>", methods=['GET'])
@cross_origin()
def find_keyword_articles(keywords):
    if request.method != 'GET':
        return "<p>Invalid Request</p>"
    keywords = list(keywords.split(","))
    data = query_keywords(keywords)
    return data

@app.route("/signup", methods=['POST'])
@cross_origin()
def create_user():
    if request.method != 'POST':
        app.logger.error("Invalid Request type made on /signup")
        return "<p>Invalid Request made use POST</p>"
    elif not request.is_json:
        app.logger.error("Invalid mime type recieved on /signup")
        return "<p>Invalid mime type. Application/type must be JSON</p>" 
    
    payload = request.get_json()
    try:
        name = payload['name']
        password = (hashlib.sha256(payload['password'].encode('utf-8'))).hexdigest()
        email = payload['email']
    except Exception as e:
        app.logger.error("Request with partial payload encountered on /signup")
        app.logger.error(e)
        return "<p>Incomplete payload recieved on. Be sure to fill out the username, password and email fields</p>" 
    
    response = insert_user(name, email, password)
    if not response:
        return "<p> Internal Server Error <p>"
    return response

def update_user():
    pass

@app.route("/publish", methods=['PUT'])
@cross_origin()
def create_paper():
    if request.method != "PUT":
        app.logger.error("Invalid Request type made on /signup")
        return "<p>Invalid Request made use PUT</p>"
    elif not request.is_json:
        app.logger.error("Invalid mime type recieved on /signup")
        return "<p>Invalid mime type. Application/type must be JSON</p>"
    
    payload = request.get_json()

    try:
        title = payload['title']
        year = payload['year']
        fos_name = payload['fos_name']
        n_citation = int(payload['n_citation'])
        url = payload['url']
        author_id = payload['author_id']

        page_start = payload.get('page_start', None)
        if page_start:
            page_start = int(page_start)
        page_end = payload.get('page_end', None)
        if page_end:
            page_end = int(page_end)
        doc_type = payload.get('doc_type', None)
        lang = payload.get('lang', None)
        vol = payload.get('vol', None)
        if page_end:
            vol = int(vol)
        issue = payload.get('issue', None)
        if issue:
            issue = int(issue)
        issn = payload.get('issn', None)
        isbn = payload.get('isbn', None)
        doi = payload.get('doi', None)
        abstract = payload.get('abstract', None)

    except Exception as e:
        app.logger.error("Request with partial payload encountered on /signup")
        app.logger.error(e)
        return "<p>Incomplete payload recieved on. Be sure to fill out the username, password and email fields</p>" 
    
    response = publish_paper(author_id, title, year, fos_name, n_citation, url, page_start, page_end, 
                                doc_type, lang, vol, issue, issn, isbn, doi, abstract)
    if not response:
        return "<p> Internal Server Error <p>"
    return response
