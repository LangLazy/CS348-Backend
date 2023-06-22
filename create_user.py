import mysql.connector
import os
import logging
import uuid

from db import database

def insert_user(name, email, hashedpass):
    try:
        log = logging.getLogger(__name__)
        log.error("HELLOE PLEASE", name, email, hashedpass)
        db = database()

        query = ["Select * from user where email = %s"]
        result = db.execute(query, [name])
        log.error("initial scan", result)

        if result != []:
            return "Invalid email provided, already exists!"

        new_uuid = str(uuid.uuid4())
        query = "Insert into author(author_id, author_name) VALUES(%s, %s)"
        result = db.execute(query, [new_uuid, name])
        log.error("author insert", result)

        query = "Insert into user(author_id, email, user_pass) VALUES(%s, %s, %s)"
        result = db.execute(query, [new_uuid, email, hashedpass])
        log.error("user insert", result)
        return "success"

    except Exception as e:
        log.error(e)
        return None
