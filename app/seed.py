from sqlalchemy.orm import Session
from app.models.Userdb import User as UserDb
from app.models.Issuedb import Issue as IssueDb

def seed(db: Session):
    if db.query(UserDb).first() is not None or db.query(IssueDb).first() is not None:
        return
    users = [
        UserDb(email = "test1@test.com", password="test1A$c34"),
        UserDb(email = "test2@test.com", password="test1A$c35"),
        UserDb(email = "test3@test.com", password="test1A$c36"),
        UserDb(email = "test4@test.com", password="test1A$c37"),
        UserDb(email = "test5@test.com", password="test1A$c38"),
        UserDb(email = "test6@test.com", password="test1A$c39"),
    ]
    db.add_all(users)
    db.commit()
    user_1 = db.query(UserDb).filter(UserDb.email == "test1@test.com" ).first()
    user_2 = db.query(UserDb).filter(UserDb.email == "test2@test.com" ).first()
    user_3 = db.query(UserDb).filter(UserDb.email == "test3@test.com" ).first()
    user_4 = db.query(UserDb).filter(UserDb.email == "test4@test.com" ).first()
    user_5 = db.query(UserDb).filter(UserDb.email == "test5@test.com" ).first()
    user_6 = db.query(UserDb).filter(UserDb.email == "test6@test.com" ).first()
    
    issues = [
        IssueDb(title="Server keeps crashing", description="Cant seem to make a stable connection", type="Bug", user_id=user_1.id),
        IssueDb(title="can you create me an account", description="Requesting for a new account", type="Service request", user_id=user_2.id),
        IssueDb(title="Server data has been corrupted", description="data been corrupted", type="Incident report", user_id=user_3.id),
        IssueDb(title="can you create me an account", description="Requesting for a new account", type="Service request", user_id=user_4.id),
        IssueDb(title="can you create me an account", description="Requesting for a new account", type="Service request", user_id=user_5.id),
        IssueDb(title="can you create me an account", description="Requesting for a new account", type="Service request", user_id=user_6.id),
        
        
    ]
    db.add_all(issues)
    db.commit()