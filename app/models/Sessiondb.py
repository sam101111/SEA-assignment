from sqlalchemy import  Column, Integer, String, DateTime
from database import Base

class User(Base):
    __tablename__ = "sessions"

    user_id = Column(Integer )
    session_id = Column(String, unique=True, index=True, primary_key=True)
    expire_time = Column(DateTime)


