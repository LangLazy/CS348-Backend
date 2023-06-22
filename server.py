from flask import Flask, request
from flask_cors import CORS, cross_origin
import hashlib

from query_keywords import query_keywords
from create_user import insert_user

app = Flask(__name__)
cors = CORS(app)

@app.route("/keywords/<keywords>", methods=['GET'])
@cross_origin()
def find_keyword_articles(keywords):
    if request.method != 'GET':
        return "<p>Invalid Request</p>"
    keywords = list(keywords.split(","))
    data = query_keywords(keywords, app)
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
        name = payload['username']
        password = hashlib.sha256(payload['password'])
        email = payload['email']
    except:
        app.logger.error("Request with partial payload encountered on /signup")
        return "<p>Incomplete payload recieved on. Be sure to fill out the username, password and email fields</p>" 
    
    response = insert_user(name, password, email)
    return response

def update_user():
    pass

def create_paper():
    pass
