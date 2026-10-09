from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import date

from app.models.transactions import Transaction, Transaction_type

class TransactionRepository:
    def __init__(self, db:Session):
        self.db= db

    def create(self, transaction:Transaction) -> Transaction:
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)

        return transaction

    def get_by_id(self, trnx_id:int,user_id:int) -> Transaction | None:
        statement = select(Transaction).where(Transaction.id == trnx_id,Transaction.user_id == user_id)
        
        return self.db.scalar(statement)

    def get_all(
        self,
        user_id: int,
        tx_type: Transaction_type | None = None,
        category_id: int | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        sort_order: str = "desc",
        offset: int = 0,
        limit: int = 20,
        ) -> list[Transaction]:

        statement = select(Transaction).where(
            Transaction.user_id == user_id
        )

        if tx_type is not None:
            statement = statement.where(
                Transaction.tx_type == tx_type
            )

        if category_id is not None:
            statement = statement.where(
                Transaction.category_id == category_id
            )

        if start_date is not None:
            statement = statement.where(
                Transaction.transaction_date >= start_date
            )

        if end_date is not None:
            statement = statement.where(
                Transaction.transaction_date <= end_date
            )

        if sort_order == "asc":
            statement = statement.order_by(
                Transaction.transaction_date.asc()
            )
        else:
            statement = statement.order_by(
                Transaction.transaction_date.desc()
            )

        statement = statement.offset(offset).limit(limit)

        return list(self.db.scalars(statement).all())

    def delete(self, transaction: Transaction) -> None:
        self.db.delete(transaction)
        self.db.commit()
        

