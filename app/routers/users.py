from fastapi import APIRouter, Cookie, Request, Depends, HTTPException, Response, Form
from typing import Annotated, Optional
from fastapi.responses import HTMLResponse
from services.users import *
from services.sessions import *
from schemas.user import *
from middleware.sessionMangement import roleCheck
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
async def delete(request: Request, id: str, db: Session = Depends(getDB)):
    isAdmin = roleCheck(True, request.cookies.get("seasonID"), db)
    if isAdmin:
        if not checkIfUserExists(db, id):
            raise HTTPException(status_code=404, detail="ID of user not found")
        deleteUser(db, id)
        return {"message": "User has been successfully deleted"}
    else:
        raise HTTPException(status_code=403, detail="User does not have necessary permission")

@router.post('/login')
async def login(response: Response, email: Annotated[str, Form()], password: Annotated[str, Form()] ,db: Session = Depends(getDB)):
    emailFormat = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    if re.match(emailFormat, email) == None:
        raise HTTPException(status_code=400, detail="Email entered is not valid format")
    if not checkIfUserExistsByEmail(db, email):
        raise HTTPException(status_code=404, detail="Email does not exist in database")

    if checkPassword(db, password, email) == False:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
        
    response.set_cookie(key="sessionID", value=f"{createSession(db, getIdByEmail(db, email))}")
    return {"message": "Session has been successfully created"}



@router.post('/logout')
async def logout(response: Response, sessionID: Optional[str] = Cookie(None), db: Session = Depends(getDB)):
    try:
        deleteSession(db,sessionID)
        response.delete_cookie("sessionID")
    except:
       raise HTTPException(status_code=404, detail="session does not exist")
    return {"message": "Session has been successfully deleted"}