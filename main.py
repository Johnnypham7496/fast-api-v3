from fastapi import FastAPI, Response, status
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



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)