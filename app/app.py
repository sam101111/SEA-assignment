from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routers.issues import router as issues_router
from routers.auth import router as auth_router


app = FastAPI()
app.include_router(issues_router, prefix="/api/issues", tags=["issues"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def home(req: Request):
    context = {'request': req}
    return templates.TemplateResponse("index.html", context)


@app.get('/issues', response_class=HTMLResponse)
def home(req: Request):
    context = {'request': req}
    return templates.TemplateResponse("issues.html", context)

@app.get('/login', response_class=HTMLResponse)
def home(req: Request):
    context = {'request': req}
    return templates.TemplateResponse("login.html", context)