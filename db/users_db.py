from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from db_config import Base


class UserDb(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(90), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    role = Column(String(120), unique=False, nullable=False)
    is_active = Column(Boolean(),default=True)
    is_superuser = Column(Boolean(),default=False)
    jobs = relationship("Job",back_populates="jobs")