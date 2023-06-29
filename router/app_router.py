from fastapi import APIRouter, Response, status

router = APIRouter()


@router.get("/", tags=['Welcome'], response_description='Displays welcome message')
async def welcome(response: Response):
    response.status_code=status.HTTP_200_OK
    return {"message": "Hello, welcome to the Justice League's FastAPI"}


@router.get("/health", tags= ['Health'], response_description='Returns the health status of this endpoint')
async def health(response: Response):
    response.status_code=status.HTTP_200_OK
    return {"status": "OK"}