from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from models.Sessiondb import Session as SessionDb

def createSession(db: Session, user_id: str):
    session = SessionDb(user_id = user_id )
    db.add(session)
    db.commit()
    return session.session_id
    

def getUserBySession(db: Session, session_id: str):
    session = db.query(SessionDb).filter(SessionDb.session_id == session_id).first()
    return session.user_id


def getUserRoleBySession():
    pass

def removeOldSessions():
    pass


def deleteSession(db: Session, session_id: str):
    toDelete = db.query(SessionDb).filter(SessionDb.session_id == session_id).first()
    db.delete(toDelete)
    db.commit()
