from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum as dbEnum
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    isAdmin = Column(Boolean, default=True)

    issues = relationship("Issue", back_populates="user")