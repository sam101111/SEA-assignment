from enum import Enum
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str

class CreateUser(UserBase):
    pass

class LoginUser(UserBase):
    pass

class DeleteUser(BaseModel):
    id: str
    


# use Pydantic to make schema