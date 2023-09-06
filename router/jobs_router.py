from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import JobsModel, MessageModel, CreateJobModel, UserModel, UpdateJobModel
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
    response.headers['message'] = 'Successfully retieved all job information'
    return return_value


@router.get('/{job_id}', response_description='Successfully retrieved by ID', description='Get by ID', status_code= 200, responses={200: {"model": JobsModel}, 400: {"model": MessageModel}, 404: {"model": MessageModel}})
def get_by_id(job_id: int, response: Response, db: Session= Depends(get_db)):
    return_value = jobs_repository.get_by_id(db, job_id)

    if return_value == None:
        response_text = f'company information with id {job_id} not found. Please check the ID number and try again.'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= response_text)
    
    response.status_code = status.HTTP_200_OK
    response.headers['message'] = 'Successfully retrieved job information by ID'
    return return_value


@router.post('/', response_description='Creates a new job description', description='Creates a new job description', response_model=JobsModel, status_code=status.HTTP_201_CREATED, responses={400: {"model": MessageModel}, 409: {"model": MessageModel}})
def create_job_description(request: CreateJobModel, response: Response, db: Session=Depends(get_db)):
    username_request = request.username
    title_request = request.title.lower()
    company_request = request.company.lower()
    location_request = request.location.lower()
    description_request = request.description.lower()

    username = users_repository.get_by_username(db, username_request)

    if username is None:
        response_text = 'username not found. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response_text)

    if username_request == '':
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
    user_model = UserModel(id=username.id, username=username.username, email=username.email, role=username.role)

    # Create a JobsModel instance with the provided job information and the UserModel instance
    job_model = JobsModel(id=0, title=title_request, company=company_request, location=location_request,
                          description=description_request, user=user_model)
    
    response.status_code = status.HTTP_201_CREATED
    response.headers['message'] = 'job created'
    return jobs_repository.add_jobs(db, job_model.title, job_model.company, job_model.location, job_model.description, job_model.user.id)


@router.put('/{job_id}', response_description='Successfully updated user company', description='Updating company record', status_code=status.HTTP_204_NO_CONTENT, responses={204: {"model": None}, status.HTTP_400_BAD_REQUEST: {"model": MessageModel}, status.HTTP_404_NOT_FOUND: {"model": MessageModel}})
def update_job(job_id: int, request: UpdateJobModel, response: Response, db: Session = Depends(get_db)):
    title_request = request.title.lower()
    company_request = request.company.lower()
    location_request = request.location.lower()
    description_request = request.description.lower()


    if title_request == None and company_request == None and location_request == None and description_request == None: 
        response_text = 'response body cannot be empty. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= response_text)
    

    job_id_check = jobs_repository.get_by_id(db, job_id)

    if job_id_check == None:
        response_text = 'username does not exist. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= response_text)
    
    if title_request != None:
        title_request = title_request.strip()
    else:
        title_request = ''

    if company_request != None:
        company_request = company_request.strip()
    else:
        company_request = ''

    if location_request != None:
        location_request = location_request.strip()

    if description_request != None:
        description_request = description_request.strip()


    if title_request == '' and company_request == '' and location_request == '' and description_request == '':
        response_text = 'response body fields cannot be empty. Please check your payload and try again.'
        raise HTTPException(status_code=400, detail=response_text)
    
    response.status_code = status.HTTP_204_NO_CONTENT
    response.headers['message'] = 'Successfully updated job details'
    return jobs_repository.update_job(db, job_id, title_request, company_request, location_request, description_request)