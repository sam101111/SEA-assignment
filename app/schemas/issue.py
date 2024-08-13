from enum import Enum
from pydantic import BaseModel
from typing import Optional

class IssueType(str, Enum):
    SERVICE_REQUEST = "Service request"
    INCIDENT_REPORT = "Incident report"
    BUG = "Bug"
    ACCOUNT_AND_ACCESS = "Account and Access"

class IssueBase(BaseModel):
    title: str
    type: IssueType
    description: str
    

class CreateIssue(IssueBase):
    user_id: int


class ReadIssues(BaseModel):
    user_id: int

class ReadAllIssues(BaseModel):
    pass

class ReadIssue(IssueBase):
    pass

class UpdateIssue(BaseModel):
    type: Optional[IssueType]
    title: Optional[str]
    description: Optional[str]

class DeleteIssue(BaseModel):
    id: int

class IssueResponse():
    pass





