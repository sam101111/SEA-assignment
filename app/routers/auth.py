from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from services.user import *
from schemas.user import *
from database import getDB

router = APIRouter()



@router.get('/')
async def home(db: Session = Depends(getDB)):
    return  getUsers(db)

@router.post('/register')
async def register(user: CreateUser, db: Session = Depends(getDB)):
    createUser(db,user.email, user.password)
    return 

@router.delete('/{id}')
async def delete(id: int, db: Session = Depends(getDB)):
    deleteUser(db, id)