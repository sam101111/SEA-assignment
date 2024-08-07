from enum import Enum

class RoleType(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
# use Pydantic to make schema