from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get('/')
def home(req: Request):
    context = {'request': req}
    return  {"message": "issues"}


@router.put('/')
def home(req: Request):
    context = {'request': req}
    return  {"message": "issues"}