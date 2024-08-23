from typing import Optional
from fastapi import APIRouter, FastAPI, Request, Depends, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.users import getRoleById, getUsers
from app.database import engine, Base, getDB
from app.models import Userdb, Issuedb
from app.routers.issues import router as issues_router
from app.routers.users import router as auth_router
from app.services.issues import getAllIssues, getIssuesByUser
from app.services.sessions import getUserBySession
from sqlalchemy.orm import Session
from app.middleware.sessionMangement import roleCheck

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get('/', response_class=HTMLResponse)
def home(req: Request, sessionID: Optional[str] = Cookie(None)):
    context = {'request': req}
    if sessionID:
        return templates.TemplateResponse(name="/index.html", request=req)
    else:
        return templates.TemplateResponse("/unauthorised.html", context)

@router.get('/issues', response_class=HTMLResponse )
def home(req: Request, db: Session = Depends(getDB), sessionID: Optional[str] = Cookie(None)):
    try:
        if sessionID:
            issues = getIssuesByUser(db, getUserBySession(db, sessionID))
            context = {'request': req, "issues": issues}
            return templates.TemplateResponse("issues.html", context)
        else:
            return templates.TemplateResponse("unauthorised.html", context)
    except:
        context = {'request': req}
        return templates.TemplateResponse("unauthorised.html", context)

@router.get('/directory', response_class=HTMLResponse )
def home(req: Request, db: Session = Depends(getDB), sessionID: Optional[str] = Cookie(None)):
        try:
            if sessionID:
                users = getUsers(db)
                userRole = getRoleById(db, getUserBySession(db, sessionID))
                context = {'request': req, "users": users, "role": userRole}
                return templates.TemplateResponse("userDirectory.html", context)
            else:
                return templates.TemplateResponse("unauthorised.html", context)

        except:
            context = {'request': req}
            return templates.TemplateResponse("unauthorised.html", context)


@router.get('/login', response_class=HTMLResponse)
def home(req: Request):
    context = {'request': req}
    return templates.TemplateResponse("login.html", context)

@router.get('/manage', response_class=HTMLResponse)
async def home( req: Request, db: Session = Depends(getDB), sessionID: Optional[str] = Cookie(None) ):
    context = {'request': req}
    try:
        isAdmin = roleCheck(True, sessionID, db )

        if isAdmin:
            issues =getAllIssues(db)
            context = {'request': req, "issues": issues}

            return templates.TemplateResponse("manage.html", context )
        else:
            return templates.TemplateResponse("unauthorised.html", context)
    except:
        return templates.TemplateResponse("unauthorised.html", context)
        
@router.get('/successfulLogin', response_class=HTMLResponse)
async def home( req: Request, db: Session = Depends(getDB) ):
    issues =getAllIssues(db)
    context = {'request': req, "issues": issues}

    return templates.TemplateResponse("successfulLogin.html", context )

@router.get('/register',  response_class=HTMLResponse)
async def register(req: Request):
    context = {'request': req}
    return templates.TemplateResponse("register.html", context)