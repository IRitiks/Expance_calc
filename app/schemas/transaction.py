from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.transactions import Transaction,Transaction_type


class TransactionCreate(BaseModel):
    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    tx_type: Transaction_type

    description: str | None = Field(
        default=None,
        max_length=255,
    )
    transaction_date: date
    categories_id:int =Field(gt=0)


class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    tx_type: Transaction_type =Field(validation_alias="trnx_type",serialization_alias="tx_type")
    description: str | None
    transaction_date: date
    user_id: int
    category_id: int

    model_config = {
        "from_attributes": True
    }

class TransactionUpdate(BaseModel):
    amount:Decimal | None =Field(default=None,gt=0,max_digits=12,decimal_places=2)
    tx_type: Transaction_type | None= None
    description:str | None= Field(default=None,max_length=255)
    transaction_date: date | None=None
    category_id:int | None = Field(default=None,gt=0)
