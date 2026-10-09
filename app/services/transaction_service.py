from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from app.models.category import Category
from app.models.transactions import Transaction, Transaction_type
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionUpdate

class TransactionService:
    def __init__(self, db:Session):
        self.db = db
        self.repositories = TransactionRepository(db)

    def create(self, transaction_data: TransactionCreate, user_id:int) -> Transaction:
        category = self.db.get(Category,transaction_data.categories_id)

        if category is None or category.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found")

        if category.trnx_type.value != transaction_data.tx_type.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction type must match category type")

        transaction = Transaction(
            amount=transaction_data.amount,
            trnx_type=transaction_data.tx_type,
            description=transaction_data.description,
            transaction_date=transaction_data.transaction_date,
            user_id=user_id,
            category_id=transaction_data.categories_id
        )

        return self.repositories.create(transaction)

    def get_by_id(self,transaction_id:int,user_id:int) -> Transaction:
        transaction = self.repositories.get_by_id(transaction_id,user_id)


        if transaction is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found")

        return transaction

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

        if start_date and end_date and start_date > end_date:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before or equal to end_date",
            )

        return self.repositories.get_all(
        user_id=user_id,
        tx_type=tx_type,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date,
        sort_order=sort_order,
        offset=offset,
        limit=limit,
        )

    def update(
        self,
        transaction_id: int,
        transaction_data: TransactionUpdate,
        user_id: int,
        ) -> Transaction:

        transaction = self.get_by_id(
        transaction_id,
        user_id,
        )

        changes = transaction_data.model_dump(
        exclude_unset=True
        )

    
        for field in (
        "amount",
        "tx_type",
        "transaction_date",
        "category_id",
        ):
            if field in changes and changes[field] is None:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"{field} cannot be null",
                )

        new_category_id = changes.get(
            "category_id",
            transaction.category_id,
            )

        new_tx_type = changes.get(
        "tx_type",
        transaction.trnx_type,
        )

        category = self.db.get(Category, new_category_id)

        if category is None or category.user_id != user_id:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
            )

        if category.trnx_type.value != new_tx_type.value:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction type must match category type",
            )

        for field, value in changes.items():
            setattr(transaction, field, value)

            self.db.commit()
            self.db.refresh(transaction)

        return transaction


    def delete(
        self,
        transaction_id: int,
        user_id: int,
        ) -> None:

        transaction = self.get_by_id(
        transaction_id,
        user_id,
        )

        self.repositories.delete(transaction)