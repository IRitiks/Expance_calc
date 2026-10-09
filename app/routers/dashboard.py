from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.dashboard import (
    DashboardSummary,
    CategoryExpenseSummary,
    MonthlySummary,
)
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummary,
)
def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = DashboardService(db)
    return service.get_summary(current_user.id)


@router.get(
    "/category-expenses",
    response_model=list[CategoryExpenseSummary],
)
def get_category_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = DashboardService(db)
    return service.get_category_expenses(current_user.id)


@router.get(
    "/monthly-summary",
    response_model=list[MonthlySummary],
)
def get_monthly_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = DashboardService(db)
    return service.get_monthly_summary(current_user.id)