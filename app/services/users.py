from sqlalchemy.orm import Session
from models.Userdb import User as UserDb
from schemas.user import *
from sqlalchemy.sql import exists

def createUser(db: Session, email: str, password: str):
    user = UserDb(email = email, password = password, isAdmin = True)
    db.add(user)
    db.commit()

def deleteUser(db: Session, id: int):

    toDelete = db.query(UserDb).filter(UserDb.id == id).first()
    db.delete(toDelete)
    db.commit()

def updateUser(db: Session, id: int, toUpdate):
    db.query(UserDb).filter(UserDb.id == id).update(toUpdate)
    db.commit()

def getUsers(db: Session):
    return db.query(UserDb).all()

def getUser(db: Session, id: int):
    return db.query(UserDb).filter(UserDb.id == id).scalar()

def checkIfUserExists(db: Session, id: int):
    return db.query(exists().where(UserDb.id == id)).scalar()