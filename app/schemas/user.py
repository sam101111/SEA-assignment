from enum import Enum
from pydantic import BaseModel


class User(BaseModel):
    pass

class CreateUser(BaseModel):
    email: str
    password: str


class DeleteUser(BaseModel):
    id: int
    


# use Pydantic to make schema