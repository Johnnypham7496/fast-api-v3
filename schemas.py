from pydantic import BaseModel
from typing import Optional

class UserModel(BaseModel):
    id: int
    username: str
    email: str
    role: str
    
    class Config:
        orm_mode = True


class JobsModel(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    user: UserModel

    class Config:
        orm_mode = True


class MessageModel(BaseModel):
    detail: str


class CreateUserModel(BaseModel):
    username: str
    email: str
    role: str


class CreateJobModel(BaseModel):
    username: str
    title: str
    company: str
    location: str
    description: str


class UpdateUserModel(BaseModel):
    email: Optional[str]
    role: Optional[str]


class UpdateJobModel(BaseModel):
    title: Optional[str]
    company: Optional[str]
    location: Optional[str]
    description: Optional[str]