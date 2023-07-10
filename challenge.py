from db import database

def get_challenge():
    db = database()
    result = db.get_random(2)
    print(result)
    return result