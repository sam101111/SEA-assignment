from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from models.Issuedb import Issue as IssueDb
from models.Userdb import User as UserDb
from schemas.issue import IssueType
def getAllIssues(db: Session ):
    return db.query(IssueDb).all()

def getIssuesByUser(db: Session, id: str):
    return db.query(IssueDb).filter(IssueDb.user_id == id).all()

def createIssue(db: Session, title: str, description: str, type: IssueType, user_id: str ):
    newIssue = IssueDb(title = title, description = description, type = type.value, user_id = user_id )
    db.add(newIssue)
    db.commit()

def getIssueByID(db: Session, id: str):
    return db.query(IssueDb).filter(IssueDb.id == id).scalar()

def updateIssue(db: Session, id: str, toUpdate):
    db.query(IssueDb).filter(IssueDb.id == id).update(toUpdate)
    db.commit()
    

def deleteIssue(db: Session, id: str):
    toDelete = db.query(IssueDb).filter(IssueDb.id == id).first()
    db.delete(toDelete)
    db.commit()

def checkIfIssueExists(db: Session, id: str):
    return db.query(exists().where(IssueDb.id == id)).scalar()