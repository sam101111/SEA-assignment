from sqlalchemy import  Column, ForeignKey, Integer, String, Enum as dbEnum
from sqlalchemy.orm import relationship
from schemas.issue import IssueType
from database import Base
import uuid

class Issue(Base):
    __tablename__ = "issues"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=False)
    type = Column(dbEnum(IssueType), index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="issues")
