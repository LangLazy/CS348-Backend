from db import database
import logging
from operation_types import Operation_Types

"""
Wrapper function log user actions. Called after any major operation (api call).
Input: 
    - userId -> from the user table which is also an authorId
    - operation -> expects an enum from operation_types
    - summary -> description of change that the user can see
"""
def log_action(userId, operation, summary):
    logging.basicConfig(level=logging.DEBUG, force=True)
    logging.getLogger(__name__).setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)

    if operation not in iter(Operation_Types):
        raise Exception("operation expected to be part of Operation_Types class")

    try:
        db = database()
        timestamp = "NOW()" # confirmed that this works
        
        query = '''Insert into history(user_id, timestamp, operation_type, summary)
                                VALUES(%s, %s, %s, %s)'''

        db.execute(query, [userId, timestamp,  operation.value, summary], False)
        return "sucess"
    except Exception as e:
        log.error("I have failed brother")
        log.debug(e)
        return None