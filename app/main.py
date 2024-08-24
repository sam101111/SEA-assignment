from fastapi import FastAPI
from app.database import engine, Base
from app.routers.issues import router as issues_router
from app.routers.users import router as auth_router
from app.routers.pages import router as pages_router


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(issues_router, prefix="/api/issues", tags=["issues"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(pages_router, tags=["pages"])
