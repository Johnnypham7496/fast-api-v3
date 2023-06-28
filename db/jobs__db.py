from sqlalchemy import Column,Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.users_db import Base


class User(Base):
    id = Column(Integer,primary_key = True, index=True)
    title = Column(String,nullable= False)
    company = Column(String,nullable=False)
    location = Column(String,nullable = False)
    description = Column(String,nullable=False)
    date_posted = Column(Date)
    is_active = Column(Boolean(),default=True)
    owner_id =  Column(Integer,ForeignKey("user.id"))
    owner = relationship("User",back_populates="jobs")
