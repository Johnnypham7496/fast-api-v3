from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import JobsModel, MessageModel, CreateJobModel, UserModel
from repository import jobs_repository, users_repository
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


@router.post('/', response_description='Creates a new job description', description='Creates a new job description', response_model=JobsModel, status_code=status.HTTP_201_CREATED, responses={400: {"model": MessageModel}, 409: {"model": MessageModel}})
def create_job_description(request: CreateJobModel, response: Response, db: Session=Depends(get_db)):
    user_id_request = request.user_id
    title_request = request.title
    company_request = request.company
    location_request = request.location
    description_request = request.description

    user_id = users_repository.get_by_user_id(db, user_id_request)

    if user_id is None:
        response_text = 'user_id not found. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response_text)

    if user_id_request == '':
        response_text = 'user_id field cannot be empty. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_text)
    
    if title_request == '':
        response_text = 'title field cannot be empty. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_text)
    
    if company_request == '':
        response_text = 'company field cannot be empty. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_text)
    
    if location_request == '':
        response_text = 'location field cannot be empty. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_text)
    
    if description_request == '':
        response_text = 'description field cannot be empty. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_text)
    
    # Create a UserModel instance from the user information fetched from the database
    user_model = UserModel(id=user_id.id, username=user_id.username, email=user_id.email, role=user_id.role)

    # Create a JobsModel instance with the provided job information and the UserModel instance
    job_model = JobsModel(id=0, title=title_request, company=company_request, location=location_request,
                          description=description_request, user=user_model)
    
    response.status_code = status.HTTP_201_CREATED
    response.headers['message'] = 'job created'
    return jobs_repository.add_jobs(db, job_model.title, job_model.company, job_model.location, job_model.description, job_model.user.id)
