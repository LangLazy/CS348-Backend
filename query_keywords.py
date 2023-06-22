import mysql.connector
import os
import logging

from db import database

def query_keywords(keywords: list[str], app):
    db = database()

    query = generate_keyword_query_string(keywords)
    app.logger.error("QWUERY: "+  query)
    result = db.execute(query, keywords)
    app.logger.error("QWUERY: ",  result)
    output = []
    
    for row in result:
        output.append(row)
    
    return output

def generate_keyword_query_string(keywords):
    if len(keywords) == 0:
        return ("SELECT * FROM paper NATURAL JOIN keywords")
    formatted_portion = ["t.word = %s"] * len(keywords)
    query_params = " OR ".join(formatted_portion)
    query = ("SELECT * FROM paper NATURAL JOIN keywords  as t WHERE " + query_params)
    return query

    