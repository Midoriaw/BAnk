from sqlalchemy import Compiled, Integer, String, ForeignKey, Text, DateTime, Column, Float, Enum
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime


import enum

class CardStatus(enum.Enum):
    active = "active"
    blocked = "blocked"


class Base(DeclarativeBase):
    pass


class RegORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)


    cards = relationship("Opencard", back_populates="user")
    credits = relationship("Credit", back_populates="user", cascade="all, delete-orphan")


class Opencard(Base):
    __tablename__ = "card"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_number = Column(String(16), unique=True, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    cvv = Column(String(4), nullable=False)
    status = Column(Enum(CardStatus), default=CardStatus.active)

    user = relationship("RegORM", back_populates="cards")



class Credit(Base):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)                # сумма кредита
    interest_rate = Column(Float, nullable=False)         # процентная ставка
    create_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)           # дата погашения

    user = relationship("RegORM", back_populates="credits")


