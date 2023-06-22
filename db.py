import mysql.connector
import os
import logging


def connect_db():
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
    return cursor