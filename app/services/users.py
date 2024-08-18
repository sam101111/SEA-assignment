from sqlalchemy.orm import Session
from models.Userdb import User as UserDb
from schemas.user import *
from sqlalchemy.sql import exists
import hashlib

def createUser(db: Session, email: str, password: str):
    user = UserDb(email = email, password = password, isAdmin = True)
    db.add(user)
    db.commit()

def deleteUser(db: Session, id: str):

    toDelete = db.query(UserDb).filter(UserDb.id == id).first()
    db.delete(toDelete)
    db.commit()

def updateUser(db: Session, id: str, toUpdate):
    db.query(UserDb).filter(UserDb.id == id).update(toUpdate)
    db.commit()

def getUsers(db: Session):
    return db.query(UserDb).all()

def getUser(db: Session, id: str):
    return db.query(UserDb).filter(UserDb.id == id).scalar()

def checkIfUserExists(db: Session, id: str):
    return db.query(exists().where(UserDb.id == id)).scalar()

def checkIfUserExistsByEmail(db: Session, email: str ):
    return db.query(exists().where(UserDb.email == email)).first()

def checkPassword(db: Session, password: str, email: str):
    user = db.query(UserDb).filter(UserDb.email == email).first()
    if user.password == hashlib.sha256(password.encode()).hexdigest():
        return True
    else:
        return False
    
def getIdByEmail(db: Session, email: str):
    user = db.query(UserDb).filter(UserDb.email == email).first()
    return user.id

def getRoleById(db: Session, id: str):
    user = db.query(UserDb).filter(UserDb.id == id).first()
    return user.isAdmin
