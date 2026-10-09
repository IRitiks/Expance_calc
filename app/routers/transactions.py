from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException,status,Depends, Query
from datetime import date

from app.models.transactions import Transaction_type
from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse, TransactionUpdate
)
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions",tags=["Transactions"])

@router.post(
    "/",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TransactionService(db)

    return service.create(
        transaction_data,
        current_user.id,
    )


@router.get(
    "/",
    response_model=list[TransactionResponse],
)
def get_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TransactionService(db)

    return service.get_all(current_user.id)


@router.get(
    "/",
    response_model=list[TransactionResponse],
)
def get_transactions(
    tx_type: Transaction_type | None = None,
    category_id: int | None = Query(default=None, gt=0),
    start_date: date | None = None,
    end_date: date | None = None,
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TransactionService(db)

    return service.get_all(
        user_id=current_user.id,
        tx_type=tx_type,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date,
        sort_order=sort_order,
        offset=(page - 1) * limit,
        limit=limit,
    )

@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id:int,
    transaction_data:TransactionUpdate,
    current_user:User=Depends(get_current_user),
    db:Session= Depends(get_db)
):
    service= TransactionService(db)

    return service.update(
        transaction_id,
        transaction_data,
        current_user.id
    )


@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TransactionService(db)

    service.delete(
        transaction_id,
        current_user.id,
    )