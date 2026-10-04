from app.core.db import Base
from enum import Enum
from datetime import datetime
from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column,relationship


from app.core.db import Base


class Category_type(str,Enum):
    EXPENSE="expense"
    INCOME="income"

class Category(Base):
    __tablename__ = "categories"
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True,index=True)
    name:Mapped[str]=mapped_column(String(50),nullable=False)
    trnx_type:Mapped[Category_type]=mapped_column(SQLEnum(Category_type),nullable=False)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True,nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,nullable=False)
    

user: Mapped["User"] = relationship(
    back_populates="categories"
)

transactions: Mapped[list["Transaction"]] = relationship(
    back_populates="Category"
)