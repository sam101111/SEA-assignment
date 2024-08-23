import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, getDB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool




SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def login_user():
         client.post("/api/auth/register",
                           data={"email": "test2@test.com", "password": "2£23AacD"})
         loginRequest = client.post("/api/auth/login",
                           data={"email": "test2@test.com", "password": "2£23AacD"})
         assert loginRequest.status_code == 200
         sessionID = loginRequest.cookies.get("sessionID")
         assert sessionID is not None
         yield
         headers = {
              "Cookie": f"sessionID={sessionID}"
         }
         response = client.post("/api/auth/logout", headers=headers)
         assert response.status_code == 200

@pytest.fixture()
def login_admin():
         loginRequest = client.post("/api/auth/login",
                           data={"email": "admintest@test.com", "password": "test1A$c34"})
         assert loginRequest.status_code == 200
         sessionID = loginRequest.cookies.get("sessionID")
         assert sessionID is not None
         yield
         headers = {
              "Cookie": f"sessionID={sessionID}"
         }
         response = client.post("/api/auth/logout", headers=headers)
         assert response.status_code == 200
     

app.dependency_overrides[getDB] = override_get_db

client = TestClient(app)


