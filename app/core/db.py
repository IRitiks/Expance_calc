from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DB_URL= "postgresql://postgres:mypassword@localhost:5432/mydb"

engine = create_engine(DB_URL)

LocalSession = sessionmaker(autocommit= False,
autoflush=False, bind=engine)

Base=declarative_base()

def get_db():
    db=LocalSession()
    try:
        yield db
    finally:
        db.close()

