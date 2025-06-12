from fastapi import FastAPI, Depends
from src.schema import UserOUT, LogOUT, OpencardOUT, Create_credOUT, Personal_accountOUT, PersonalAccountIN
from src.crud import create_users,log_users, create_bank_card, create_credit, get_personal_account
from src.database import get_db, lifespan
from sqlalchemy.ext.asyncio import AsyncSession
from src.services import credit_service
from src.services.credit_service import generate_card_number, calculate_interes_by_term
from passlib.context import CryptContext

import logging

app = FastAPI(lifespan=lifespan)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logging.basicConfig(level=logging.DEBUG)

@app.post("/users", tags=["Регистрация"])
async def user(user:UserOUT, db: AsyncSession = Depends(get_db)):
    new_user = await create_users(db, user.username, user.password)
    return {"id": new_user.id, "username":new_user.username}

@app.post("/logusers", tags=["Авторизация"])
async def log(login:LogOUT, db: AsyncSession = Depends(get_db)):
    user = await log_users(db, login.username, login.password)
    return {
            "mess": "Вход выполнен успешно!",
            "user_id": user.id,
            "username": user.username
    }

@app.post("/card", tags=["Оформление карты"])
async def cards(cards: OpencardOUT, db:AsyncSession = Depends(get_db)):

    new_cards = await create_bank_card(db, user_id=cards.user_id, expiration_date=cards.expiration_date, cvv=cards.cvv)
    return {
        "mess": "Карта открыта успешно",
        "new_cards_id": new_cards.id,
        "card_number": new_cards.card_number

    }


@app.post("/credits", tags=["Оформление кредита"])
async def credit(credit: Create_credOUT, db: AsyncSession = Depends(get_db)):
    new_credit, active_card = await create_credit(db, user_id=credit.user_id, amount=credit.amount, due_date=credit.due_date)
    return {
        "mess": "Кредит успешно открыт",
        "credit_id": new_credit.id,
        "interest_rate": f"{new_credit.interest_rate}%",
        "due_date": new_credit.due_date,
        "card_number": active_card.card_number

    }


@app.post("/personal_account/{user_id}", response_model=Personal_accountOUT,tags=["Личный кабинет"])
async def  personal_account(user_id: int, date:PersonalAccountIN ,db: AsyncSession =Depends(get_db)):
    result = await get_personal_account(db, user_id, date.password)
    return result
