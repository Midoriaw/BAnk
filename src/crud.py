from src.schema import Personal_accountOUT
from datetime import datetime, date
from fastapi import HTTPException, Depends
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import select, intersect
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from typing_extensions import deprecated

from src.services.credit_service import calculate_interes_by_term, generate_card_number

from src.models import Base, RegORM, Credit, Opencard, CardStatus

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_users(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(RegORM).where(RegORM.username == username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="пользователь уже был зарегистрирыван")

    new_user = RegORM(username=username, password= pwd_context.hash(password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def log_users(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(RegORM).where(RegORM.username == username))
    user = result.scalar_one_or_none()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=404, detail="Неверный логин или пароль")
    return user

async def create_bank_card(db: AsyncSession, user_id: int, expiration_date:datetime.date, cvv: str):
    result = await db.execute(select(RegORM).where(RegORM.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Пользовательно не найден")

    new_card = Opencard(user_id=user_id, card_number=generate_card_number(), expiration_date=expiration_date, cvv=cvv, status=CardStatus.active)
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    return new_card


async def create_credit(db: AsyncSession, user_id: int, amount: float, due_date:date):

    result = await db.execute(select(Opencard).where(Opencard.user_id == user_id, Opencard.status==CardStatus.active))
    active_card = result.scalars().first()

    if not active_card:
        raise HTTPException(status_code=400, detail="Кредит не может быть выдан: у пользователя нет активной карты")

    create_at = datetime.utcnow()
    interest_rate = calculate_interes_by_term(create_at, due_date)

    credit = Credit(user_id=user_id, amount=amount, interest_rate=interest_rate, create_at=create_at, due_date=due_date)
    db.add(credit)
    await db.commit()
    await db.refresh(credit)
    return credit, active_card



async def get_personal_account(db: AsyncSession,user_id: int, password: str):
    result = await db.execute(select(RegORM).where(RegORM.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=404, detail="Неверный пароль")


    result_cards = (await db.execute(select(Opencard).where(Opencard.user_id == user_id)))
    cards = result_cards.scalars().all()

    result_credits = (await db.execute(select(Credit).where(Credit.user_id == user_id)))
    credits = result_credits.scalars().all()

    return {

        "id": user.id,
        "username": user.username,
        "cards": cards,
        "credits": credits
    }







