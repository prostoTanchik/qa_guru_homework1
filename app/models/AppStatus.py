from pydantic import BaseModel, EmailStr, HttpUrl


class AppStatus(BaseModel):
    database: bool
