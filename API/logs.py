from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Habit, HabitLog, User
from app.schemas import HabitLogCreate, HabitLogOut

router = APIRouter(prefix="/habits/{habit_id}/logs", tags=["Logs"])


def _get_habit_or_404(habit_id: int, user: User, db: Session) -> Habit:
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.owner_id == user.id,
    ).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.get("/", response_model=List[HabitLogOut])
def list_logs(
    habit_id: int,
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List completion logs for a habit, optionally filtered by date range."""
    _get_habit_or_404(habit_id, current_user, db)

    query = db.query(HabitLog).filter(HabitLog.habit_id == habit_id)
    if from_date:
        query = query.filter(HabitLog.logged_date >= from_date)
    if to_date:
        query = query.filter(HabitLog.logged_date <= to_date)

    return query.order_by(HabitLog.logged_date.desc()).limit(limit).all()


@router.post("/", response_model=HabitLogOut, status_code=status.HTTP_201_CREATED)
def check_in(
    habit_id: int,
    payload: HabitLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mark a habit as completed for the given date (default: today).

    Prevents duplicate logs for the same habit on the same day.
    """
    _get_habit_or_404(habit_id, current_user, db)

    existing = db.query(HabitLog).filter(
        HabitLog.habit_id == habit_id,
        HabitLog.logged_date == payload.logged_date,
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Habit already logged for {payload.logged_date}",
        )

    log = HabitLog(habit_id=habit_id, **payload.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_log(
    habit_id: int,
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a specific log entry (undo a check-in)."""
    _get_habit_or_404(habit_id, current_user, db)

    log = db.query(HabitLog).filter(
        HabitLog.id == log_id,
        HabitLog.habit_id == habit_id,
    ).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    db.delete(log)
    db.commit()
