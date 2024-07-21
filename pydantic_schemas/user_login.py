from pydantic import BaseModel


class UserLogin(BaseModel):
    password: str
    email: str
