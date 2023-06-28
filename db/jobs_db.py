from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from db_config import Base
import users_db


class JobDb(Base):
    __tablename__ = "jobs"

    id = Column(Integer,primary_key = True, index=True)
    title = Column(String,nullable= False)
    company = Column(String,nullable=False)
    location = Column(String,nullable = False)
    description = Column(String,nullable=False)
    date_posted = Column(Date)
    is_active = Column(Boolean(),default=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserDb", back_populates="jobs")