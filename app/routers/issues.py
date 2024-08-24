from fastapi import APIRouter, Request, Depends, HTTPException, Form, Cookie
from typing import Annotated
from fastapi.responses import HTMLResponse
from app.middleware.sessionMangement import roleCheck
from app.schemas.issue import *
from app.services.issues import *
from app.services.users import checkIfUserExists, getIdByEmail, getRoleById
from app.services.sessions import getUserBySession
from app.database import getDB


router = APIRouter()


@router.post("/")
async def postIssue(
    request: Request,
    title: Annotated[str, Form()],
    type: Annotated[IssueType, Form()],
    description: Annotated[str, Form()],
    db: Session = Depends(getDB),
    sessionID: Optional[str] = Cookie(None),
):
    try:
        userId = getUserBySession(db, sessionID)
        print(userId)
        return createIssue(db, title, description, type, userId)

    except:
        raise HTTPException(status_code=401, detail="Invalid session token provided")


@router.get("/{user_id}")
async def getByUser(
    user_id: str, db: Session = Depends(getDB), sessionID: Optional[str] = Cookie(None)
):
    if (
        getUserBySession(db, sessionID) == user_id
        or roleCheck(True, sessionID, db) == True
    ):
        if not checkIfUserExists(db, user_id):
            raise HTTPException(status_code=404, detail="ID of user not found")
        return getIssuesByUser(db, user_id)
    else:
        raise HTTPException(
            status_code=403, detail="User does not have necessary permission"
        )


@router.get("/")
async def getIssues(db: Session = Depends(getDB)):
    return getAllIssues(db)


@router.patch("/{id}")
async def patchIssue(
    id: str,
    title: Annotated[Optional[str], Form()] = None,
    type: Annotated[Optional[IssueType], Form()] = None,
    description: Annotated[Optional[str], Form()] = None,
    db: Session = Depends(getDB),
    sessionID: Optional[str] = Cookie(None),
):
    try:
        userId = getUserBySession(db, sessionID)
        userRole = getRoleById(db, userId)
        userIssueId = getUserByIssueID(db, id)
        if not checkIfIssueExists(db, id):
            raise HTTPException(status_code=404, detail="ID of issue not found")
    except:
        raise HTTPException(
            status_code=403, detail="User does not have necessary permission"
        )

    if userIssueId == userId or userRole == True:
        issue = {"title": title, "type": type, "description": description}
        # loops through each pair and filters out any pairs where the value is None
        filteredIssue = {
            key: value for key, value in issue.items() if value is not None
        }
        print(filteredIssue)
        print(sessionID)
        try:
            updateIssue(db, id, filteredIssue)
        except:
            raise HTTPException(status_code=422, detail="Must enter at least one value")
        raise HTTPException(status_code=200, detail="Issue has been updated")
    else:
        raise HTTPException(
            status_code=403, detail="User does not have necessary permission"
        )


@router.delete("/{id}")
async def delete(
    id: str, db: Session = Depends(getDB), sessionID: Optional[str] = Cookie(None)
):
    try:
        isAdmin = roleCheck(True, sessionID, db)
    except:
        raise HTTPException(
            status_code=403, detail="User does not have necessary permission"
        )
    if isAdmin:
        if not checkIfIssueExists(db, id):
            raise HTTPException(status_code=404, detail="ID of issue not found")
        deleteIssue(db, id)
    else:
        raise HTTPException(
            status_code=403, detail="User does not have necessary permission"
        )
