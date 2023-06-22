from flask import Flask, request
from flask_cors import CORS, cross_origin
from query_keywords import query_keywords

app = Flask(__name__)
cors = CORS(app)

@app.route("/keywords/<keywords>", methods=['GET'])
@cross_origin()
def find_keyword_articles(keywords):
    if request.method != 'GET':
        return "<p>Please man</p>"
    keywords = list(keywords.split(","))
    data = query_keywords(keywords)
    return data
    
def create_user():
    pass

def update_user():
    pass

def create_paper():
    pass
