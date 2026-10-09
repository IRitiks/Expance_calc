from app.core.db import Base
from decimal import Decimal
from enum import Enum
from sqlalchemy import (Date,DateTime,Enum as SQLEnum,ForeignKey,Numeric,String)
from sqlalchemy.orm import Mapped, mapped_column,relationship

class Transaction_type(str,Enum):
    EXPENSE="expense"
    INCOME="income"


class Transaction(Base):
    __tablename__ = "transactions"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True,index=True)
    description:Mapped[str|None]=mapped_column(String(250),nullable=True)
    amount:Mapped[Decimal]=mapped_column(Numeric(8,2),nullable=False)
    trnx_type:Mapped[Transaction_type]=mapped_column(SQLEnum(Transaction_type),nullable=False)
    transaction_date:Mapped[Date]=mapped_column(Date,nullable=False)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    category_id:Mapped[int]=mapped_column(ForeignKey("categories.category_id",ondelete="RESTRICT"),nullable=False,index=True)


user: Mapped["User"] = relationship(
    back_populates="transactions"
)

category: Mapped["Category"] = relationship(
    back_populates="transactions"
)