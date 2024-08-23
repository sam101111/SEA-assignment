from app.services.users import getRoleById
from app.services.sessions import getUserBySession
from sqlalchemy.orm import Session


def roleCheck(protected: bool, sessionId: str, db: Session):
    userID = getUserBySession(db,sessionId)
    userRole = getRoleById(db, userID)
    if userRole == protected:
        return True
    else:
        return False
    
# return the userID from the session ID