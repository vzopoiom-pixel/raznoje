from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Habit, HabitLog, User
from app.schemas import HabitStats

router = APIRouter(prefix="/stats", tags=["Stats"])


def _calculate_streak(log_dates: list[date]) -> tuple[int, int]:
    """Return (current_streak, longest_streak) from a sorted list of logged dates."""
    if not log_dates:
        return 0, 0

    sorted_dates = sorted(set(log_dates), reverse=True)
    today = date.today()

    # Current streak: consecutive days ending today or yesterday
    current = 0
    expected = today
    for d in sorted_dates:
        if d == expected:
            current += 1
            expected -= timedelta(days=1)
        elif d == today - timedelta(days=1) and current == 0:
            # Allow starting from yesterday
            current += 1
            expected = d - timedelta(days=1)
        else:
            break

    # Longest streak: scan all dates
    longest = 1
    temp = 1
    for i in range(1, len(sorted_dates)):
        if (sorted_dates[i - 1] - sorted_dates[i]).days == 1:
            temp += 1
            longest = max(longest, temp)
        else:
            temp = 1

    return current, longest


@router.get("/", response_model=List[HabitStats])
def all_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return aggregate statistics for all active habits of the current user."""
    habits = (
        db.query(Habit)
        .filter(Habit.owner_id == current_user.id, Habit.is_archived == False)
        .all()
    )
    return [_build_stats(h, db) for h in habits]


@router.get("/{habit_id}", response_model=HabitStats)
def habit_stats(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return detailed statistics for a single habit."""
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.owner_id == current_user.id,
    ).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return _build_stats(habit, db)


def _build_stats(habit: Habit, db: Session) -> HabitStats:
    logs = db.query(HabitLog).filter(HabitLog.habit_id == habit.id).all()
    log_dates = [log.logged_date for log in logs]

    current_streak, longest_streak = _calculate_streak(log_dates)

    # Completion rate: unique days logged in last 30 days / 30
    thirty_days_ago = date.today() - timedelta(days=30)
    recent = {d for d in log_dates if d >= thirty_days_ago}
    completion_rate = round(len(recent) / 30 * 100, 1)

    return HabitStats(
        habit_id=habit.id,
        title=habit.title,
        total_completions=len(log_dates),
        current_streak=current_streak,
        longest_streak=longest_streak,
        completion_rate_last_30d=completion_rate,
        last_completed=max(log_dates) if log_dates else None,
    )
