from fastapi import APIRouter, Response, status, Depends
from sqlalchemy.orm import Session
from schemas import UserModel
from repository import users_repository
from db_config import get_db
from typing import List


router = APIRouter(
    prefix='/users/v1',
    tags=['users']
)


@router.get('/', response_description='Display all users', description='Retrieves all users', response_model=List[UserModel])
def get_all_users(response: Response, db: Session= Depends(get_db)):
    return_value = users_repository.get_all_users(db)
    response.status_code=status.HTTP_200_OK
    return return_value