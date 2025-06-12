from datetime import date, datetime

from pydantic import BaseModel
from typing import List

class UserOUT(BaseModel):
    username: str
    password: str


class LogOUT(BaseModel):
    username: str
    password: str


class OpencardOUT(BaseModel):
    user_id: int
    expiration_date: date
    cvv: str

    class Config:
        from_orm=True


class Create_credOUT(BaseModel):
    user_id: int
    amount: float
    due_date: date

    class Config:
        from_orm=True


class Personal_accountOUT(BaseModel):
    id: int
    username: str
    cards: List[OpencardOUT]
    credits: List[Create_credOUT]

    class Config:
        from_orm=True


class PersonalAccountIN(BaseModel):
    password: str