import dotenv
dotenv.load_dotenv()
import json
from http import HTTPStatus
from app.database.engine import create_db_and_tables
from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, add_pagination, paginate
from app.models.AppStatus import AppStatus
from routers import status, users
from app.models.User import User
# from database import users_db


app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)
add_pagination(app)




if __name__ == "__main__":
    import uvicorn
    create_db_and_tables()
    uvicorn.run(app, host="127.0.0.1", port=8000)