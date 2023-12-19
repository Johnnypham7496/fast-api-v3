from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import UserModel, MessageModel, CreateUserModel, UpdateUserModel
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
    response.headers['message'] = 'Successfully displayed all users'
    return return_value


@router.get('/{username}', response_description='Displays user by username', description='Retrieves user by username', response_model=UserModel, responses= {404: {"model": MessageModel}})
def get_by_username(response: Response, username: str, db: Session= Depends(get_db)):

    if (return_value := users_repository.get_by_username(db, username)) == None:
        response_text = 'username not found. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response_text)
    
    response.headers['message'] = 'user found'
    response.status_code = status.HTTP_200_OK
    return return_value


@router.post('/', response_description='Creates a new user', description='Creates a new user', response_model=UserModel, status_code=status.HTTP_201_CREATED, responses= {400: {"model": MessageModel}, 409: {"model": MessageModel}})
def create_user(request: CreateUserModel, response: Response, db: Session= Depends(get_db)):
    username_request = request.username
    email_request = request.email
    role_request = request.role

    existing_username = users_repository.get_by_username(db, username_request)
    existing_email = users_repository.get_by_email(db, email_request)

    if existing_username!= None:
        response_text = 'username already exists. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=response_text)
    
    if existing_email!= None:
        response_text = 'email already exists. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=response_text)
    
    if username_request.strip() == '':
        response_text = 'username cannot be empty. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_text)
    
    if email_request.strip() == '':
        response_text = 'email cannot be empty. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_text)
    
    if role_request.strip() == '':
        response_text = 'role cannot be empty. Please check your parameter and try again.'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_text)
    
    response.status_code = status.HTTP_201_CREATED
    response.headers['Location'] = '/users/v1/' + str(username_request.strip())
    return users_repository.add_user(db, username_request, email_request, role_request)


@router.put('/{username}', response_description="Successfully updated user info", description="Update a single user record", status_code=204, responses={204: {"model": None}, 400: {"model": MessageModel}, 404: {"model": MessageModel}})
def update_user(username: str, request: UpdateUserModel, response: Response, db:Session = Depends(get_db)):
    email_request = request.email
    role_request = request.role

    if email_request == None and role_request == None:
        response_text = 'request body cannot be empty. Please check your payload and try again'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_text)
    

    if (user_check := users_repository.get_by_username(db, username)) == None:
        response_text = 'username not found. Please check your username and try again.'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= response_text)
    
    if email_request != None:
        email_request = email_request.strip()
    else:
        email_request = ''

    if role_request != None:
        role_request = role_request.strip()
    else:
        role_request = ''

    if email_request == '' and role_request == '':
        response_text = 'request body fields cannot be empty. Please check your payload and try again'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_text)
    
    response.status_code= status.HTTP_204_NO_CONTENT
    response.headers['message'] = 'Successfully updated user profile'
    return users_repository.update_user(db, username, email_request, role_request)


@router.delete('/{username}', response_description='Successfully deleted user', description='Deletes user by username', status_code= 204, responses={204: {"model": None}, 404: {"model": MessageModel}})
def delete_user(username: str, response: Response, db: Session = Depends(get_db)):

    if (return_value := users_repository.get_by_username(db, username)) == None:
        response_text = 'username not found. Please check your parameter and try again'
        raise HTTPException(status_code= 404, detail= response_text)
    
    response.status_code = status.HTTP_204_NO_CONTENT
    response.headers['message'] = 'Successfully deleted user'
    return users_repository.delete_user(db, username)
