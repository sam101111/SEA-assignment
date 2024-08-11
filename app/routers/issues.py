from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from schemas.issue import *
from services.issues import *
from database import getDB


router = APIRouter()

@router.post('/')
async def postIssue(issue: CreateIssue, db: Session = Depends(getDB) ):
    return  createIssue(db, issue.title, issue.description, issue.type, issue.user_id)


@router.get('/{user_id}')
async def getByUser(user_id: int, db: Session = Depends(getDB)):
    return getIssuesByUser(db, user_id)

@router.get('/')
async def getIssues(db: Session = Depends(getDB)):
    return  getAllIssues(db)


@router.patch('/{id}') 
async def patchIssue(id: int, issue: UpdateIssue, db: Session = Depends(getDB)):
    if not checkIfExists(db, id):
        raise HTTPException(status_code=404, detail="ID of issue not found")
    formattedIssue = issue.dict()
    formattedIssue['type'] = issue.type.value
    return updateIssue(db, id, formattedIssue)

@router.delete('/{id}')
async def delete(id: int, db: Session = Depends(getDB)):
    if not checkIfExists(db, id):
        raise HTTPException(status_code=404, detail="ID of issue not found")

    deleteIssue(db, id)
