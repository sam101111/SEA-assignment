from enum import Enum
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(pattern=r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$")
    password: str


class GetAllUsersResponse(UserBase):
    isAdmin: bool
    id: str


class CreateUser(UserBase):
    pass


class LoginUser(UserBase):
    pass


class DeleteUser(BaseModel):
    id: str


# use Pydantic to make schema
