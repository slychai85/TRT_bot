from sqlalchemy import Column, Integer, String, DateTime, func
from app.database.base import Base
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255))
    full_name = Column(String(255))
    referrals_count = Column(Integer, default=0)
    referrals_week = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    joined_at = Column(DateTime, default=func.now())