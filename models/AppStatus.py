from pydantic import BaseModel, EmailStr, HttpUrl


class AppStatus(BaseModel):
    users: bool
