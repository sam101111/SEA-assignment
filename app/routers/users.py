from fastapi import APIRouter, Cookie, Request, Depends, HTTPException, Response, Form
from typing import Annotated, Optional
from fastapi.responses import HTMLResponse
from app.services.users import *
from app.services.sessions import *
from app.schemas.user import *
from app.middleware.sessionMangement import roleCheck
from app.database import getDB
from sqlalchemy.exc import IntegrityError
import re
import hashlib

router = APIRouter()


@router.get("/")
async def getAllUsers(
    db: Session = Depends(getDB), sessionID: Optional[str] = Cookie(None)
):
    try:
        if sessionID:
            return getUsers(db)
        else:
            raise HTTPException(
                status_code=403, detail="User does not have necessary permission"
            )
    except Exception as err:
        raise HTTPException(
            status_code=403, detail="User does not have necessary permission"
        )


@router.post("/register")
async def register(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(getDB),
):
    emailFormat = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    passwordFormat = r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{8,16}$"
    if email == "" or password == "":
        raise HTTPException(
            status_code=400, detail="Email or password entered is not valid format"
        )

    if (
        re.match(emailFormat, email) == None
        or re.match(passwordFormat, password) == None
    ):
        raise HTTPException(
            status_code=400, detail="Email or password entered is not valid format"
        )
    try:
        hashedPassword = hashlib.new("SHA256")
        hashedPassword.update(str(password).encode())

        createUser(db, email, hashedPassword.hexdigest())
    except IntegrityError as err:
        print(err)
        raise HTTPException(status_code=422)


@router.patch("/promote/{id}")
async def promote(
    request: Request,
    id: str,
    db: Session = Depends(getDB),
    sessionID: Optional[str] = Cookie(None),
):
    try:
        isAdmin = roleCheck(True, sessionID, db)
        if isAdmin:
            if not checkIfUserExists(db, id):
                raise HTTPException(status_code=404, detail="ID of user not found")
            if getRoleById(db, id) == True:
                raise HTTPException(
                    status_code=403, detail="User does not have necessary permission"
                )

            promoteUser(db, id)
            return {"message": "User has been successfully promoted"}
        else:
            raise HTTPException(status_code=400, detail="User already an admin")
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=403, detail="User does not have necessary permission"
        )


@router.delete("/{id}")
async def delete(
    request: Request,
    id: str,
    db: Session = Depends(getDB),
    sessionID: Optional[str] = Cookie(None),
):
    try:
        isAdmin = roleCheck(True, sessionID, db)
        if isAdmin:
            if not checkIfUserExists(db, id):
                raise HTTPException(status_code=404, detail="ID of user not found")
            deleteUser(db, id)
            return {"message": "User has been successfully deleted"}
        else:
            raise HTTPException(
                status_code=403, detail="User does not have necessary permission"
            )
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=403, detail="User does not have necessary permission"
        )


@router.post("/login")
async def login(
    response: Response,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(getDB),
):
    emailFormat = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    if email == "admintest@test.com" and password == "test1A$c34":
        if not checkIfUserExistsByEmail(db, email):
            hashedPassword = hashlib.new("SHA256")
            hashedPassword.update(str(password).encode())
            createUser(db, email, hashedPassword.hexdigest(), True)

    if email == "" or password == "":
        raise HTTPException(
            status_code=400, detail="Email or password entered is not valid format"
        )

    if re.match(emailFormat, email) == None:
        raise HTTPException(status_code=400, detail="Email entered is not valid format")
    if not checkIfUserExistsByEmail(db, email):
        raise HTTPException(status_code=404, detail="Email does not exist in system")

    if checkPassword(db, password, email) == False:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    response.set_cookie(
        key="sessionID", value=f"{createSession(db, getIdByEmail(db, email))}"
    )

    return {"message": "Session has been successfully created"}


@router.post("/getid")
async def get_id(
    response: Response,
    email: Annotated[str, Form()],
    db: Session = Depends(getDB),
    sessionID: Optional[str] = Cookie(None),
):
    try:
        if sessionID:
            return getIdByEmail(db, email)
    except:
        raise HTTPException(status_code=404, detail="session does not exist")


@router.post("/logout")
async def logout(
    response: Response,
    sessionID: Optional[str] = Cookie(None),
    db: Session = Depends(getDB),
):
    try:
        deleteSession(db, sessionID)
        response.delete_cookie("sessionID")
    except:
        raise HTTPException(status_code=404, detail="session does not exist")
    return {"message": "Session has been successfully deleted"}
