import mysql.connector
import os
import logging
import uuid

from db import connect_db

def insert_user(name, email, hashedpass):
    cursor = connect_db()
    query = "Select * from user where email = %s"
    cursor.execute(query, [name])
    for row in cursor:
        return "Invalid email provided, already exists!"

    new_uuid = uuid.uuid4()
    try:
        query = "Insert into author(author_id, author_name) VALUES(%s, %s)"
        cursor.execute(query, [new_uuid, name])

        query = "Insert into user(author_id, email, user_pass) VALUES(%s, %s)"
        cursor.execute(query, [new_uuid, email, hashedpass])
        return "success"
    except Exception as e:
        return e
