from sqlalchemy import case, extract, func, select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.transactions import Transaction, Transaction_type


class DashboardRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_summary(self, user_id: int) -> dict:
        income_expr = func.coalesce(
            func.sum(
                case(
                    (
                        Transaction.trnx_type == Transaction_type.INCOME,
                        Transaction.amount,
                    ),
                    else_=0,
                )
            ),
            0,
        ).label("total_income")

        expense_expr = func.coalesce(
            func.sum(
                case(
                    (
                        Transaction.trnx_type == Transaction_type.EXPENSE,
                        Transaction.amount,
                    ),
                    else_=0,
                )
            ),
            0,
        ).label("total_expenses")

        statement = select(
            income_expr,
            expense_expr,
        ).where(
            Transaction.user_id == user_id
        )

        result = self.db.execute(statement).one()

        income = result.total_income
        expenses = result.total_expenses

        return {
            "total_income": income,
            "total_expenses": expenses,
            "net_balance": income - expenses,
        }

    def get_category_expenses(self, user_id: int) -> list[dict]:
        statement = (
            select(
                Category.category_id.label("category_id"),
                Category.name.label("category_name"),
                func.sum(Transaction.amount).label("total_amount"),
            )
            .join(
                Category,
                Transaction.category_id == Category.category_id,
            )
            .where(
                Transaction.user_id == user_id,
                Category.user_id == user_id,
                Transaction.trnx_type == Transaction_type.EXPENSE,
            )
            .group_by(Category.category_id, Category.name)
            .order_by(func.sum(Transaction.amount).desc())
        )

        results = self.db.execute(statement).all()

        return [
            {
                "category_id": row.category_id,
                "category_name": row.category_name,
                "total_amount": row.total_amount,
            }
            for row in results
        ]

    def get_monthly_summary(self, user_id: int) -> list[dict]:
        month_expr = func.date_trunc(
            "month",
            Transaction.transaction_date,
        ).label("month")

        income_expr = func.coalesce(
            func.sum(
                case(
                    (
                        Transaction.trnx_type == Transaction_type.INCOME,
                        Transaction.amount,
                    ),
                    else_=0,
                )
            ),
            0,
        ).label("total_income")

        expense_expr = func.coalesce(
            func.sum(
                case(
                    (
                        Transaction.trnx_type == Transaction_type.EXPENSE,
                        Transaction.amount,
                    ),
                    else_=0,
                )
            ),
            0,
        ).label("total_expenses")

        statement = (
            select(month_expr, income_expr, expense_expr)
            .where(Transaction.user_id == user_id)
            .group_by(month_expr)
            .order_by(month_expr)
        )

        results = self.db.execute(statement).all()

        return [
            {
                "month": row.month.strftime("%Y-%m"),
                "total_income": row.total_income,
                "total_expenses": row.total_expenses,
                "net_balance": row.total_income - row.total_expenses,
            }
            for row in results
        ]  