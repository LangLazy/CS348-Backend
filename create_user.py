import mysql.connector
import os
import logging
import uuid

from db import database

def insert_user(name, email, hashedpass):
    db = database()

    query = "Select * from user where email = %s"
    result = db.execute(query, [name])

    if result != []:
        return "Invalid email provided, already exists!"

    new_uuid = uuid.uuid4()
    
    try:
        query = "Insert into author(author_id, author_name) VALUES(%s, %s)"
        db.cursor.execute(query, [new_uuid, name])

        query = "Insert into user(author_id, email, user_pass) VALUES(%s, %s, %s)"
        db.cursor.execute(query, [new_uuid, email, hashedpass])
        return "success"

    except Exception as e:
        return e
