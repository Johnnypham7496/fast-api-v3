from fastapi import FastAPI
from router import app_router, users_router
import uvicorn



app = FastAPI(
    title="Justice Leagues FastAPI",
    description="This is the swagger doc for the Justice League",
    version='1.0.0'
)


app.include_router(app_router.router)
app.include_router(users_router.router)


# @app.get("/dbsetup")
# async def db_setup(db: Session = Depends(get_db)):
#     users_db.Base.metadata.drop_all(engine)
#     users_db.Base.metadata.create_all(engine)
#     users_repository.add_user_td(db)
#     response_text = '{"message": "Database Created"}'
#     response = Response(content=response_text, status_code=status.HTTP_200_OK, media_type='application/json')
#     return response


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)