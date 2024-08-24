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


def test_get_users_unsuccessfully(test_db):
    response = client.get("/api/auth")
    assert response.status_code == 403

def test_register_user(test_db):
    response = client.post("/api/auth/register",
                           data={"email": "test2@test.com", "password": "2£23AacD"})
    assert response.status_code == 200

def test_register_user_with_bad_password(test_db):
    response = client.post("/api/auth/register",
                           data={"email": "test@test.com", "password": "password"})
    assert response.status_code == 400

def test_register_user_with_bad_email(test_db):
    response = client.post("/api/auth/register",
                           data={"email": "test", "password": "2£23AacD"})
    assert response.status_code == 400

def test_register_user_with_no_data(test_db):
    response = client.post("/api/auth/register",
                           data={"email": "", "password": ""})
    assert response.status_code == 422

def test_register_user_exists(test_db):
            client.post("/api/auth/register",
                           data={"email": "test5@test.com", "password": "2£23AacD"})
            response = client.post("/api/auth/register",
                           data={"email": "test5@test.com", "password": "2£23AacD"})
            assert response.status_code == 422
       

def test_get_users(test_db, login_user ):
            response = client.get("/api/auth")
            assert response.status_code == 200


def test_delete_user_as_admin(test_db, login_admin):

            user = client.post("/api/auth/register",
                           data={"email": "test5@test.com", "password": "2£23AacD"})
            assert user.status_code == 200
              
            get_id = client.post("/api/auth/getid", data={"email": "test5@test.com"})
     
            assert get_id.status_code == 200
            id = get_id.content.decode().replace('"',"")
            response = client.delete(f"/api/auth/{id}")
            assert response.status_code == 200

def test_delete_user_as_user(test_db, login_user):
            user = client.post("/api/auth/register",
                           data={"email": "test5@test.com", "password": "2£23AacD"})
            assert user.status_code == 200
              
            get_id = client.post("/api/auth/getid", data={"email": "test5@test.com"})
     
            assert get_id.status_code == 200
            id = get_id.content.decode().replace('"',"")
            response = client.delete(f"/api/auth/{id}")
            assert response.status_code == 403

def test_promote_user_as_admin(test_db, login_admin):
            user = client.post("/api/auth/register",
                           data={"email": "test5@test.com", "password": "2£23AacD"})
            assert user.status_code == 200

            get_id = client.post("/api/auth/getid", data={"email": "test5@test.com"})
            assert user.status_code == 200
            id = get_id.content.decode().replace('"',"")

            response = client.patch(f"/api/auth/promote/{id}")
            assert response.status_code == 200

def test_promote_user_as_admin(test_db, login_user):
            user = client.post("/api/auth/register",
                           data={"email": "test5@test.com", "password": "2£23AacD"})
            assert user.status_code == 200

            get_id = client.post("/api/auth/getid", data={"email": "test5@test.com"})
            assert get_id.status_code == 200
            id = get_id.content.decode().replace('"',"")

            response = client.patch(f"/api/auth/promote/{id}")
            assert response.status_code == 403

def test_logout_not_exist(test_db):
        client.post("/api/auth/register",
                           data={"email": "test2@test.com", "password": "2£23AacD"})
        response = client.post("/api/auth/logout")
        assert response.status_code == 404

def test_logout_exist(test_db):
        client.post("/api/auth/register",
                           data={"email": "test2@test.com", "password": "2£23AacD"})
                
        loginRequest = client.post("/api/auth/login",
                        data={"email": "test2@test.com", "password": "2£23AacD"})
        sessionID = loginRequest.cookies.get("sessionID")
        assert sessionID is not None

        response = client.post("/api/auth/logout")
        assert response.status_code == 200

def test_login_user_with_bad_password(test_db):
    client.post("/api/auth/register",
                           data={"email": "test2@test.com", "password": "2£23AacD"})
    response = client.post("/api/auth/login",
                           data={"email": "test2@test.com", "password": "password"})
    assert response.status_code == 401

def test_login_user_with_bad_email(test_db):
    client.post("/api/auth/register",
                           data={"email": "test2@test.com", "password": "2£23AacD"})
    response = client.post("/api/auth/login",
                           data={"email": "test", "password": "2£23AacD"})    
    assert response.status_code == 400

def test_login_user_with_no_data(test_db):
    client.post("/api/auth/register",
                           data={"email": "test2@test.com", "password": "2£23AacD"})
    response = client.post("/api/auth/login",
                           data={"email": "", "password": ""})
    assert response.status_code == 422
        
      



