from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.models import FrequencyEnum


# ─── Auth ────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=100)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


# ─── Habits ──────────────────────────────────────────────────────────────────

class HabitCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    frequency: FrequencyEnum = FrequencyEnum.daily
    days_of_week: Optional[str] = Field(
        None,
        description="Weekday numbers 0-6 separated by commas, e.g. '0,2,4'",
        pattern=r"^[0-6](,[0-6])*$",
    )
    target_streak: int = Field(default=0, ge=0)
    color: str = Field(default="#6366f1", pattern=r"^#[0-9a-fA-F]{6}$")

    @field_validator("days_of_week")
    @classmethod
    def validate_custom_days(cls, v, info):
        freq = info.data.get("frequency")
        if freq == FrequencyEnum.custom and not v:
            raise ValueError("days_of_week is required when frequency is 'custom'")
        return v


class HabitUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    frequency: Optional[FrequencyEnum] = None
    days_of_week: Optional[str] = Field(None, pattern=r"^[0-6](,[0-6])*$")
    target_streak: Optional[int] = Field(None, ge=0)
    color: Optional[str] = Field(None, pattern=r"^#[0-9a-fA-F]{6}$")
    is_archived: Optional[bool] = None


class HabitOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    frequency: FrequencyEnum
    days_of_week: Optional[str]
    target_streak: int
    color: str
    is_archived: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Habit Logs ───────────────────────────────────────────────────────────────

class HabitLogCreate(BaseModel):
    logged_date: date = Field(default_factory=date.today)
    note: Optional[str] = Field(None, max_length=500)


class HabitLogOut(BaseModel):
    id: int
    habit_id: int
    logged_date: date
    note: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Stats ────────────────────────────────────────────────────────────────────

class HabitStats(BaseModel):
    habit_id: int
    title: str
    total_completions: int
    current_streak: int
    longest_streak: int
    completion_rate_last_30d: float
    last_completed: Optional[date]
