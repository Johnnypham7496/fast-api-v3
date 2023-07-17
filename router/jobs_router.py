from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import JobsModel, MessageModel
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


@router.get('/{company}', response_description='Displays company information', description='Retrieves job by company name', response_model=JobsModel, responses= {404: {"model": MessageModel}})
def get_by_company(response: Response, company: str, db: Session= Depends(get_db)):
    return_value = jobs_repository.get_by_company(db, company)

    if return_value == None:
        response_text = 'company information not found. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response_text)
    
    response.headers['message'] = 'company found'
    response.status_code = status.HTTP_200_OK
    return return_value