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
    data = query_keywords(keywords)
    return data

@app.route("/keywords", methods=['GET'])
@cross_origin()
def find_keyword_articles():
    if request.method != 'GET':
        return "<p>Invalid Request</p>"
    data = query_keywords([])
    return data


@app.route("/signup", methods=['POST'])
@cross_origin()
def create_user():
    if request.method != 'POST':
        return "<p>Invalid Request</p>"
    try:
        name = request.form['username']
        password = hashlib.sha256(request.form['password'])
        email = request.form['email']
    except:
        app.logger.error("Payload body does not have required fields")
        return
    response = insert_user(username, password, email)
    return response

def update_user():
    pass

def create_paper():
    pass
