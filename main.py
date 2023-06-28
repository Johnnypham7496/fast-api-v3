from fastapi import FastAPI, Response, status
from db import users_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, Depends
from db_config import engine, get_db
from repository import users_repository
import uvicorn



app = FastAPI(
    title="Justice Leagues FastAPI",
    description="This is the swagger doc for the Justice League",
    version='1.0.0'
)


@app.get("/", tags=['Welcome'], response_description='Displays welcome message')
async def welcome(response: Response):
    response.status_code=status.HTTP_200_OK
    return {"message": "Hello, welcome to the Justice League's FastAPI"}


@app.get("/health", tags= ['Health'], response_description='Returns the health status of this endpoint')
async def health(response: Response):
    response.status_code=status.HTTP_200_OK
    return {"status": "OK"}


@app.get("/dbsetup")
async def db_setup(db: Session = Depends(get_db)):
    users_db.Base.metadata.drop_all(engine)
    users_db.Base.metadata.create_all(engine)
    users_repository.add_user_td(db)
    response_text = '{"message": "Database Created"}'
    response = Response(content=response_text, status_code=status.HTTP_200_OK, media_type='application/json')
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)