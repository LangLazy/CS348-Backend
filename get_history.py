from db import database

def get_history(user_id):
    db = database()
    query = '''
            SELECT * FROM history WHERE user_id = %s
            '''
    result = db.execute(query, [user_id])
    return result