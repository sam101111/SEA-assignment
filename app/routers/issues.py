from fastapi import APIRouter, Request, Depends, HTTPException, Form, Cookie
from typing import Annotated
from fastapi.responses import HTMLResponse
from middleware.sessionMangement import roleCheck
from schemas.issue import *
from services.issues import *
from services.users import checkIfUserExists, getIdByEmail
from services.sessions import getUserBySession
from database import getDB


router = APIRouter()

@router.post('/')
async def postIssue(request: Request ,title: Annotated[str, Form()], type: Annotated[IssueType, Form()], description: Annotated[str, Form()] ,db: Session = Depends(getDB), sessionID: Optional[str] = Cookie(None) ):
    try:
        userId = getUserBySession(db,sessionID)
        print(userId)
        createIssue(db, title, description, type, userId)
    except:
        raise HTTPException(status_code=401, detail="Invalid session token provided")



@router.get('/{user_id}')
async def getByUser(user_id: str, db: Session = Depends(getDB)):
    if not checkIfUserExists(db, user_id):
        raise HTTPException(status_code=404, detail="ID of user not found")
    return getIssuesByUser(db, user_id)

@router.get('/')
async def getIssues(db: Session = Depends(getDB)):
    return  getAllIssues(db)


@router.patch('/{id}') 
async def patchIssue(id: str, issue: UpdateIssue, db: Session = Depends(getDB)):
    if not checkIfIssueExists(db, id):
        raise HTTPException(status_code=404, detail="ID of issue not found")
    formattedIssue = issue.dict()
    formattedIssue['type'] = issue.type.value
    return updateIssue(db, id, formattedIssue)

@router.delete('/{id}')
async def delete(id: str, db: Session = Depends(getDB), sessionID: Optional[str] = Cookie(None)):
    try:
        isAdmin = roleCheck(True, sessionID, db)
        if isAdmin:
            if not checkIfIssueExists(db, id):
                raise HTTPException(status_code=404, detail="ID of issue not found")
            deleteIssue(db, id)
        else:
            raise HTTPException(status_code=403, detail="User does not have necessary permission")
    except:
        raise HTTPException(status_code=404, detail="session does not exist")
