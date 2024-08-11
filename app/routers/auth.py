from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from services.user import *
from schemas.user import *
from database import getDB
from sqlalchemy.exc import IntegrityError
import re

router = APIRouter()



@router.get('/')
async def home(db: Session = Depends(getDB)):
    return  getUsers(db)

@router.post('/register')
async def register(user: CreateUser, db: Session = Depends(getDB)):
    emailFormat = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"

    if re.match(emailFormat, user.email) == None:
        raise HTTPException(status_code=400, detail="Email entered is not valid format")
    try:
        createUser(db,user.email, user.password)
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Email entered is already registered")


@router.delete('/{id}')
async def delete(id: int, db: Session = Depends(getDB)):
    deleteUser(db, id)