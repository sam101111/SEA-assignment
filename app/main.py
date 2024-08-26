from fastapi import FastAPI
from app.seed import seed
from app.database import SessionLocal, engine, Base
from app.routers.issues import router as issues_router
from app.routers.users import router as auth_router
from app.routers.pages import router as pages_router
from contextlib import asynccontextmanager


# This seeds the database with mock data if there isn't already data in the database
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed(db)
        yield
    finally:
        db.close()


# Creates the database tables and fastAPI instance
Base.metadata.create_all(bind=engine)
app = FastAPI(lifespan=lifespan)

# Adds the routers to the fastAPI instance
app.include_router(issues_router, prefix="/api/issues", tags=["issues"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(pages_router, tags=["pages"])
