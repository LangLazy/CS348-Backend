import mysql.connector
import os
import logging

def query_keywords(keywords: list[str], app):
    try:
        USER = os.getenv('SQL_USER')
        PASSWORD = os.getenv('SQL_PASSWORD')
        HOST = os.getenv('SQL_HOST')
        PORT = os.getenv('SQL_PORT')
    except:
        print("Could not access env vars")
        return "Internal Server Error"
    
    db = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        port=PORT,
        database="citationmonkeydb"
    )
    cursor = db.cursor()

    query = generate_keyword_query_string(keywords)
    app.logger.debug(query)
    cursor.execute(query, keywords)

    output = []
    
    for row in cursor:
        output.append(row)
    
    return output

def generate_keyword_query_string(keywords):
    if len(keywords) == 0:
        return ("SELECT * FROM paper NATURAL JOIN keywords")
    formatted_portion = ["t.word = %s"] * len(keywords)
    query_params = "OR ".join(formatted_portion)
    query = ("SELECT * FROM paper NATURAL JOIN keywords  as t WHERE" + query_params)
    return query

    