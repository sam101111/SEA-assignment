from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from services.users import *
from services.sessions import *
from schemas.user import *
from database import getDB
from sqlalchemy.exc import IntegrityError
import re
import hashlib

router = APIRouter()



@router.get('/')
async def getAllUsers(db: Session = Depends(getDB)):
    return  getUsers(db)

@router.post('/register')
async def register(user: CreateUser, db: Session = Depends(getDB)):
    emailFormat = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    passwordFormat = r""

    if re.match(emailFormat, user.email) == None:
        raise HTTPException(status_code=400, detail="Email entered is not valid format")
    try:
        hashedPassword = hashlib.new("SHA256")
        hashedPassword.update(str(user.password).encode())
 
        createUser(db,user.email, hashedPassword.hexdigest())
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Email entered is already registered")


@router.delete('/{id}')
async def delete(id: str, db: Session = Depends(getDB)):
    if not checkIfUserExists(db, id):
        raise HTTPException(status_code=404, detail="ID of user not found")
    deleteUser(db, id)

@router.post('/login')
async def login(user: LoginUser, db: Session = Depends(getDB)):
    if not checkIfUserExistsByEmail(db, user.email):
        raise HTTPException(status_code=404, detail="Email does not exist in database")
    try:
        checkPassword(db, user.password, user.email)
    except:
        pass
    createSession(db, getIdByEmail(db, user.email))


@router.delete('/logout')
async def logout():
    pass