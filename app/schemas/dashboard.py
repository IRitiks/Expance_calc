from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    net_balance: Decimal


class CategoryExpenseSummary(BaseModel):
    category_id: int
    category_name: str
    total_amount: Decimal


class MonthlySummary(BaseModel):
    month: str
    total_income: Decimal
    total_expenses: Decimal
    net_balance: Decimal