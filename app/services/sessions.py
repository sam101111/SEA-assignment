from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from models.Sessiondb import Session as SessionDb

def createSession(db: Session, user_id: str):
    session = SessionDb(user_id = user_id )
    db.add(session)
    db.commit()
    

def getUserBySession():
    pass


def getUserRoleBySession():
    pass

def removeOldSessions():
    pass
