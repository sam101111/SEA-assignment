from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from schemas.issue import *
from services.issues import *
from database import getDB


router = APIRouter()

@router.post('/')
async def postIssue(issue: CreateIssue, db: Session = Depends(getDB) ):
    return  createIssue(db, issue.title, issue.description, issue.type, issue.user_id)


@router.get('/{user_id}')
async def getIssuesByUser(user_id: int, db: Session = Depends(getDB)):
    return getIssuesByUser(db, user_id)

@router.get('/')
async def getIssues(db: Session = Depends(getDB)):
    return  getAllIssues(db)


@router.patch('/') 
def patchIssue(issue: UpdateIssue):
    context = {'request': issue}
    return  {"message": "issues"}

@router.delete('/{id}')
async def delete(id: int, db: Session = Depends(getDB)):
    deleteIssue(db, id)
