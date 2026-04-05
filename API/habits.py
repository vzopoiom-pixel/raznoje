from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Habit, User
from app.schemas import HabitCreate, HabitOut, HabitUpdate

router = APIRouter(prefix="/habits", tags=["Habits"])


def _get_habit_or_404(habit_id: int, user: User, db: Session) -> Habit:
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.owner_id == user.id,
    ).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.get("/", response_model=List[HabitOut])
def list_habits(
    include_archived: bool = Query(False, description="Include archived habits"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all habits for the current user."""
    query = db.query(Habit).filter(Habit.owner_id == current_user.id)
    if not include_archived:
        query = query.filter(Habit.is_archived == False)
    return query.order_by(Habit.created_at.desc()).all()


@router.post("/", response_model=HabitOut, status_code=status.HTTP_201_CREATED)
def create_habit(
    payload: HabitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new habit."""
    habit = Habit(**payload.model_dump(), owner_id=current_user.id)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


@router.get("/{habit_id}", response_model=HabitOut)
def get_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific habit by ID."""
    return _get_habit_or_404(habit_id, current_user, db)


@router.patch("/{habit_id}", response_model=HabitOut)
def update_habit(
    habit_id: int,
    payload: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Partially update a habit (only provided fields are changed)."""
    habit = _get_habit_or_404(habit_id, current_user, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(habit, field, value)
    db.commit()
    db.refresh(habit)
    return habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Permanently delete a habit and all its logs."""
    habit = _get_habit_or_404(habit_id, current_user, db)
    db.delete(habit)
    db.commit()
