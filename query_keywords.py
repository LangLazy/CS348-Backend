import mysql.connector
import os

def query_keywords(keywords: list[str]):
    try:
        USER = os.getenv('SQL_USERNAME')
        PASSWORD = os.getenv('SQL_PASSWORD')
        HOST = os.getenv('SQL_HOST')
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
    cursor = cnx.cursor()

    query = generate_keyword_query_string(keywords)
    cursor.execute(query, keywords)

    output = []
    
    for row in cursor:
        output.append(row)
    
    return output



def generate_keyword_query_string(keywords):
    query = ("SELECT * FROM paper NATURAL JOIN keywords"
             "WHERE ")
    formatted_portion = ["word = %s "] * len(keywords)
    query_params = "OR ".join(formatted_portion)

    return query + query_params

    