
from datetime import datetime
from sqlalchemy import Boolean,String,Float,DateTime,Text
#from typing import List,Dict,Text
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.core.db import Base



class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True,index=True)
    username:Mapped[str]=mapped_column(String(50),nullable=False,unique=True)
    email:Mapped[str]=mapped_column(String(50),nullable=False)
    hashed_password:Mapped[str]=mapped_column(String(255),nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,nullable=False)
     
transactions: Mapped[list["Transaction"]] = relationship(
    back_populates="user",
    cascade="all, delete-orphan"
)

categories: Mapped[list["Category"]] = relationship(
    back_populates="user",
    cascade="all, delete-orphan"
)