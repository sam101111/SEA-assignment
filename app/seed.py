from sqlalchemy.orm import Session
from app.models.Userdb import User as UserDb
from app.models.Issuedb import Issue as IssueDb


def seed(db: Session):
    # Checks if there is already data in the database, if so returns nothing
    if db.query(UserDb).first() is not None or db.query(IssueDb).first() is not None:
        return
    users = [
        UserDb(email="test1@test.com", password="test1A$c34"),
        UserDb(email="test2@test.com", password="test1A$c35"),
        UserDb(email="test3@test.com", password="test1A$c36"),
        UserDb(email="test4@test.com", password="test1A$c37"),
        UserDb(email="test5@test.com", password="test1A$c38"),
        UserDb(email="test6@test.com", password="test1A$c39"),
    ]
    # Adds the list of users to the database then commits it
    db.add_all(users)
    db.commit()
    user_1 = db.query(UserDb).filter(UserDb.email == "test1@test.com").first()
    user_2 = db.query(UserDb).filter(UserDb.email == "test2@test.com").first()
    user_3 = db.query(UserDb).filter(UserDb.email == "test3@test.com").first()
    user_4 = db.query(UserDb).filter(UserDb.email == "test4@test.com").first()
    user_5 = db.query(UserDb).filter(UserDb.email == "test5@test.com").first()
    user_6 = db.query(UserDb).filter(UserDb.email == "test6@test.com").first()

    issues = [
        IssueDb(
            title="Server keeps crashing",
            description="No idea why",
            type="Bug",
            user_id=user_1.id,
            is_resolved=False,
        ),
        IssueDb(
            title="Server got struck my lighting",
            description="server is very much fried",
            type="Incident report",
            user_id=user_2.id,
        ),
        IssueDb(
            title="Split my starbucks on the server",
            description="my coffee is everywhere",
            type="Incident report",
            user_id=user_3.id,
            is_resolved=True,
        ),
        IssueDb(
            title="can you create me an account",
            description="Requesting for a new account",
            type="Service request",
            user_id=user_4.id,
            is_resolved=False,
        ),
        IssueDb(
            title="can you create me an account",
            description="Requesting for a new account",
            type="Service request",
            user_id=user_5.id,
            is_resolved=False,
        ),
        IssueDb(
            title="can you create me an account",
            description="Requesting for a new account",
            type="Service request",
            user_id=user_6.id,
            is_resolved=False,
        ),
    ]
    db.add_all(issues)
    db.commit()
