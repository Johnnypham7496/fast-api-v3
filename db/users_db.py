from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from db_config import Base
import jobs_db

class UserDb(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(90), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    role = Column(String(120), unique=False, nullable=False)
    is_active = Column(Boolean(),default=True)
    is_superuser = Column(Boolean(),default=False)


    # Define the relationship between UserDb and JobDb
    jobs = relationship("JobDb", back_populates="user")



# class JobDb(Base):
#     __tablename__ = "jobs"

#     id = Column(Integer,primary_key = True, index=True)
#     title = Column(String,nullable= False)
#     company = Column(String,nullable=False)
#     location = Column(String,nullable = False)
#     description = Column(String,nullable=False)
#     date_posted = Column(Date)
#     is_active = Column(Boolean(),default=True)

#     user_id = Column(Integer, ForeignKey("users.id"))
#     user = relationship("UserDb", back_populates="jobs")
