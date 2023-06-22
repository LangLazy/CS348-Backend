import logging

from db import database

def verify_login(email, password):
    logging.basicConfig(level=logging.DEBUG, force=True)
    logging.getLogger(__name__).setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)
    try:
        db = database()
        query = ("SELECT u.user_pass FROM user as u WHERE u.email = %s")
        result = db.execute(query, [email])
        for r in result:
            if r == password:
                return "Login Validated"
        return "Login Rejected"
    except Exception as e:
        log.error("I have failed brother")
        log.debug(e)
        return None