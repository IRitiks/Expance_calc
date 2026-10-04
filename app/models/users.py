from core.db import Base
from datetime import datetime
from sqlalchemy import Boolean,Integer,Column,String,Float,DateTime,Text
#from typing import List,Dict,Text

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    username=Column(String(25),nullable=False,unique=True)
    email=Column(String(50),nullable=False)
    password=Column(String(30),nullable=False)
     
