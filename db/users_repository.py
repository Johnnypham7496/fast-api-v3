from sqlalchemy import Column, String, Integer, ForeignKey
from db_config import Base


class UserDb(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(90), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    role = Column(String(120), unique=False, nullable=False)