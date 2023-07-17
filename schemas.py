from pydantic import BaseModel


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
    user_id: int
    title: str
    company: str
    location: str
    description: str
