from enum import Enum
from pydantic import BaseModel

class IssueType(str, Enum):
    SERVICE_REQUEST = "Service request"
    INCIDENT_REPORT = "Incident report"
    BUG = "Bug"
    ACCOUNT_AND_ACCESS = "Account and Access"

class IssueBody():
    pass


class IssueResponse():
    pass





