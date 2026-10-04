from core.db import Base
from datetime import datetime
from sqlalchemy import Boolean,Integer,Column,String,Float,DateTime,Text

class Expence(Base):
    __tablename__ = "expences"

    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    title=Column(String(50),nullable=False)
    description=Column(Text,nullable=True)
    amount=Column(Float,nullable=False)
    spended_on=Column(DateTime,nullable=False,default=DateTime.utcnow)

