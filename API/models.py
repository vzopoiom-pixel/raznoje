from datetime import date, datetime
from sqlalchemy import (
    Boolean, Column, Date, DateTime, Enum, ForeignKey,
    Integer, String, Text, func,
)
from sqlalchemy.orm import DeclarativeBase, relationship
import enum


class Base(DeclarativeBase):
    pass


class FrequencyEnum(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"
    custom = "custom"  # tracks days_of_week field


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    habits = relationship("Habit", back_populates="owner", cascade="all, delete-orphan")


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    frequency = Column(Enum(FrequencyEnum), default=FrequencyEnum.daily, nullable=False)
    # Comma-separated weekday numbers: "0,1,2" = Mon, Tue, Wed
    days_of_week = Column(String(20), nullable=True)
    target_streak = Column(Integer, default=0)  # 0 = unlimited
    color = Column(String(7), default="#6366f1")  # hex color for UI
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"), nullable=False)
    logged_date = Column(Date, nullable=False, default=date.today)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    habit = relationship("Habit", back_populates="logs")
