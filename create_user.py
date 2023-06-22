import mysql.connector
import os
import logging
import uuid

from db import database

def insert_user(name, email, hashedpass):
    logging.basicConfig(level=logging.DEBUG, force=True)
    logging.getLogger(__name__).setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)
    try:
        db = database()
        log.debug("DONE 0")
        log.debug(name)
        query = ("SELECT * FROM user as u WHERE u.email = %s")
        result = db.execute(query, [name])
        log.debug("DONE 1")
        if result != []:
            return "Invalid email provided, already exists!"

        new_uuid = uuid.uuid4().hex()
        query = "Insert into author(author_id, author_name) VALUES(%s, %s)"
        result = db.execute(query, [new_uuid, name])
        log.debug("DONE 2")
        log.error("author insert", result)

        query = "Insert into user(author_id, email, user_pass) VALUES(%s, %s, %s)"
        result = db.execute(query, [new_uuid, email, hashedpass])
        log.debug("DONE 3")
        log.error("user insert", result)
        return "success"

    except Exception as e:
        log.error("I have failed brother")
        log.debug(e)
        return None
