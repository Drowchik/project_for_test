from datetime import datetime
from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    name: str
    email: EmailStr


class SUserRegister(SUser):
    password: str


class SNote(BaseModel):
    title: str
    description: str


class SNotes(SNote):
    created_at: datetime
