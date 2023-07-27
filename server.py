from flask import Flask, request
from flask_cors import CORS, cross_origin
import hashlib
import json

from query_keywords import query_keywords
from create_user import insert_user
from add_paper import publish_paper
from get_citations import find_citations
from verify_login import verify_login
from challenge import get_challenge, process_result, get_leaderboard
from update_paper import update_paper

app = Flask(__name__)
cors = CORS(app)

@app.route("/keywords", methods=['POST'])
@cross_origin()
def find_keyword_articles():
    if request.method != 'POST':
        app.logger.error("Invalid Request type made on /keywords")
        return "<p>Invalid Request</p>"
    payload = request.get_json()
    # TODO: validate that the payload is correct type
    data = query_keywords(payload)
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

@app.route("/login", methods=['POST'])
@cross_origin()
def validate_login():
    if request.method != 'POST':
        app.logger.error("Invalid Request type made on /login")
        return "<p>Invalid Request made use POST</p>"
    elif not request.is_json:
        app.logger.error("Invalid mime type recieved on /login")
        return "<p>Invalid mime type. Application/type must be JSON</p>"
    payload = request.get_json()
    try:
        email = payload['email']
        password = (hashlib.sha256(payload['password'].encode('utf-8'))).hexdigest()
    except Exception as e:
        app.logger.error("Request with partial payload encountered on /signup")
        app.logger.error(e)
        return "<p>Incomplete payload recieved on. Be sure to fill out the password and email fields</p>"
    return verify_login(email, password)

@app.route("/citations/<paper_id>", methods=['GET'])
@cross_origin()
def get_citations(paper_id):
    if request.method != 'GET':
        app.logger.error("Invalid Request type made on /citations")
        return "<p>Invalid Request</p>"
    response = find_citations(paper_id)
    return response

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
        if vol:
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
        return "<p>Incomplete payload recieved on. Be sure to fill out the title, year, fos_name, n_citation, url, and author_id fields</p>" 
    
    response = publish_paper(author_id, title, year, fos_name, n_citation, url, page_start, page_end, 
                                doc_type, lang, vol, issue, issn, isbn, doi, abstract)
    if not response:
        return "<p> Internal Server Error <p>"
    return response

@app.route("/challenge", methods=["GET"])
@cross_origin()
def propose_challenge():
    return get_challenge()

@app.route("/result", methods=["POST"])
@cross_origin()
def process_challenge_result():
    payload = request.get_json()
    try:
        winner = payload['winner']
        loser = payload['loser']
    except:
        return "Malformatted json body"
    res = process_result(winner, loser)
    return res

@app.route("/leaderboard", methods=["GET"])
@cross_origin()
def generate_leaderboard():
    return get_leaderboard()

@app.route("/update", methods=["POST"])
@cross_origin()
def handle_paper_update():
    try:
        payload = request.get_json()
        pid = payload['paper_id']
        del payload['paper_id']
        return update_paper(pid, **payload)
    except Exception as e:
        print(e)
        return "<p>Invalid format of JSON body passed<p>"


