from app.services.users import get_role_by_id
from app.services.sessions import get_user_by_session
from sqlalchemy.orm import Session


def role_check(protected: bool, sessionId: str, db: Session):
    userID = get_user_by_session(db, sessionId)
    userRole = get_role_by_id(db, userID)
    if userRole == protected:
        return True
    else:
        return False
