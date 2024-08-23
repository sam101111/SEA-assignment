from typing import Optional
from fastapi import FastAPI, Request, Depends, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.users import getRoleById, getUsers
from app.database import engine, Base, getDB
from app.models import Userdb, Issuedb
from app.routers.issues import router as issues_router
from app.routers.users import router as auth_router
from app.routers.pages import router as pages_router
from app.services.issues import getAllIssues, getIssuesByUser
from app.services.sessions import getUserBySession
from sqlalchemy.orm import Session
from app.middleware.sessionMangement import roleCheck


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(issues_router, prefix="/api/issues", tags=["issues"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(pages_router, tags=["pages"])


