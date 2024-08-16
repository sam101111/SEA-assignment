from typing import Optional
from fastapi import FastAPI, Request, Depends, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import engine, Base, getDB
from models import Userdb, Issuedb
from routers.issues import router as issues_router
from routers.users import router as auth_router
from services.issues import getAllIssues, getIssuesByUser
from services.sessions import getUserBySession
from sqlalchemy.orm import Session
from middleware.sessionMangement import roleCheck


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(issues_router, prefix="/api/issues", tags=["issues"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def home(req: Request):
    context = {'request': req}
    return templates.TemplateResponse("index.html", context)


@app.get('/issues', response_class=HTMLResponse )
def home(req: Request, db: Session = Depends(getDB), sessionID: Optional[str] = Cookie(None)):
    try:
        issues = getIssuesByUser(db, getUserBySession(db, sessionID))
        context = {'request': req, "issues": issues}
        return templates.TemplateResponse("issues.html", context)
    except:
        context = {'request': req}
        return templates.TemplateResponse("unauthorised.html", context)

@app.get('/login', response_class=HTMLResponse)
def home(req: Request):
    context = {'request': req}
    return templates.TemplateResponse("login.html", context)

@app.get('/manage', response_class=HTMLResponse)
async def home( req: Request, db: Session = Depends(getDB), sessionID: Optional[str] = Cookie(None) ):
    isAdmin = roleCheck(True, sessionID, db )
    if isAdmin:
        issues =getAllIssues(db)
        context = {'request': req, "issues": issues}

        return templates.TemplateResponse("manage.html", context )
    else:
        return templates.TemplateResponse("unauthorised.html", context)



@app.get('/successfulLogin', response_class=HTMLResponse)
async def home( req: Request, db: Session = Depends(getDB) ):
    issues =getAllIssues(db)
    context = {'request': req, "issues": issues}

    return templates.TemplateResponse("successfulLogin.html", context )