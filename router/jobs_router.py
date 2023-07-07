from fastapi import APIRouter, Response, status, Depends
from sqlalchemy.orm import Session
from schemas import JobsModel
from repository import jobs_repository
from db_config import get_db
from typing import List


router = APIRouter(
    prefix='/jobs/v1',
    tags=['jobs']
)


@router.get('/', response_description='Display all jobs', description='Retrieves all jobs', response_model=List[JobsModel])
def get_all_jobs(response: Response, db: Session= Depends(get_db)):
    return_value = jobs_repository.get_all_jobs(db)
    response.status_code=status.HTTP_200_OK
    return return_value