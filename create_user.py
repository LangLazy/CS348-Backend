import mysql.connector
import os
import logging
import uuid

from db import database

def insert_user(name, email, hashedpass):
    try:
        db = database()

        query = "Select * from user where email = %s"
        result = db.execute(query, [name])
        logging.info("initial scan", result)

        if result != []:
            return "Invalid email provided, already exists!"

        new_uuid = str(uuid.uuid4())
        query = "Insert into author(author_id, author_name) VALUES(%s, %s)"
        result = db.execute(query, [new_uuid, name])
        logging.info("author insert", result)

        query = "Insert into user(author_id, email, user_pass) VALUES(%s, %s, %s)"
        result = db.execute(query, [new_uuid, email, hashedpass])
        logging.info("user insert", result)
        return "success"

    except Exception as e:
        logging.error(e)
        return None
