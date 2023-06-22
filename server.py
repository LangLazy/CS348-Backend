from flask import Flask
import query_keywords from query_keywords

app = Flask(__name__)

@app.route("/keywords", methods=['GET'])
@cross_origin()
def query_keywords():
    if request.method != 'GET':
        return "<p>Please man</p>"
    ids = request.form.getlist('keywords', type=str)
    data = query_keywords(ids)
    return data
    
def create_user():
    pass

def update_user():
    pass

def create_paper():
    pass
