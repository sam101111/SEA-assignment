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

def test_create_issue(test_db, login_user):
      response = client.post("/api/issues", data={"title": "test issue", "type": "Bug", "description": "really good test issue"})
      assert response.status_code == 200

def test_create_issue_bad_type(test_db, login_user):
      response = client.post("/api/issues", data={"title": "test issue", "type": "wrong_type", "description": "really good test issue"})
      assert response.status_code == 422
      
def test_create_issue_bad_type(test_db, login_user):
      response = client.post("/api/issues", data={"title": "test issue", "type": "wrong_type", "description": "really good test issue"})
      assert response.status_code == 422

def test_create_issue_missing_title(test_db, login_user):
      response = client.post("/api/issues", data={"title": "", "type": "Bug", "description": "really good test issue"})
      assert response.status_code == 422

def test_create_issue_missing_description(test_db, login_user):
      response = client.post("/api/issues", data={"title": "test issue", "type": "Bug", "description": ""})
      assert response.status_code == 422

def test_create_issue_missing_type(test_db, login_user):
      response = client.post("/api/issues", data={"title": "test issue", "type": "", "description": "really good test issue"})
      assert response.status_code == 422

def test_get_user_issues(test_db, login_user):
      issue = client.post("/api/issues", data={"title": "test issue", "type": "Bug", "description": "really good test issue"})
      issue_response = issue.json()
      issue_id = issue_response
      assert issue.status_code == 200
      get_id = client.post("/api/auth/getid", data={"email": "test2@test.com"})
      assert get_id.status_code == 200
      user_id = get_id.content.decode().replace('"',"")
      expected = [{"title": "test issue", "type": "Bug", "id": f"{issue_id}", "user_id": f"{user_id}" ,"description": "really good test issue"}]
      response = client.get(f"/api/issues/{user_id}")
      assert response.status_code == 200
      response_data = response.json()
      assert response_data == expected


def test_get_user_issues_as_wrong_user(test_db):
    client.post("/api/auth/register",
                           data={"email": "test2@test.com", "password": "2£23AacD"})
    loginRequest = client.post("/api/auth/login",
                           data={"email": "test2@test.com", "password": "2£23AacD"})
    assert loginRequest.status_code == 200
      
    issue = client.post("/api/issues", data={"title": "test issue", "type": "Bug", "description": "really good test issue"})
    issue_response = issue.json()
    issue_id = issue_response
    assert issue.status_code == 200
    logout = client.post("/api/auth/logout")
    assert logout.status_code == 200
    
    create_user = client.post("/api/auth/register",
                data={"email": "test15@test.com", "password": "2£23AacD"})
    assert create_user.status_code == 200
    
    loginRequest = client.post("/api/auth/login",
                           data={"email": "test15@test.com", "password": "2£23AacD"})
    assert loginRequest.status_code == 200

    get_id = client.post("/api/auth/getid", data={"email": "test2@test.com"})
    assert get_id.status_code == 200
    user_id = get_id.content.decode().replace('"',"")
    response = client.get(f"/api/issues/{user_id}")
    assert response.status_code == 403
    response_data = response.json()
    assert response_data == {'detail': "User does not have necessary permission"}
    
def test_update_issue_title(test_db, login_user):
    create_issue = client.post("/api/issues", data={"title": "test issue", "type": "Bug", "description": "really good test issue"})
    assert create_issue.status_code == 200
    issue_id = create_issue.json()
    updated_issue = client.patch(f"/api/issues/{issue_id}", data={"title": "updating title test"})
    assert updated_issue.status_code == 200
    
def test_update_issue_wrong_type(test_db, login_user):
    create_issue = client.post("/api/issues", data={"title": "test issue", "type": "Bug", "description": "really good test issue"})
    assert create_issue.status_code == 200
    issue_id = create_issue.json()
    updated_issue = client.patch(f"/api/issues/{issue_id}", data={"type": "wrong_type"})
    assert updated_issue.status_code == 422
    
def test_update_issue_all(test_db, login_user):
    create_issue = client.post("/api/issues", data={"title": "test issue", "type": "Bug", "description": "really good test issue"})
    assert create_issue.status_code == 200
    issue_id = create_issue.json()
    updated_issue = client.patch(f"/api/issues/{issue_id}", data={"type": "Service request", "title": "updated title", "description": "updated description"})
    assert updated_issue.status_code == 200
    
def test_update_issue_as_wrong_user(test_db, login_user):
    create_issue = client.post("/api/issues", data={"title": "test issue", "type": "Bug", "description": "really good test issue"})
    assert create_issue.status_code == 200
    issue_id = create_issue.json()
    updated_issue = client.patch(f"/api/issues/{issue_id}", data={"type": "Service request", "title": "updated title", "description": "updated description"})
    assert updated_issue.status_code == 200
    


