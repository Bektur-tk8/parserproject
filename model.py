from sqlalchemy import (DECIMAL, Column, Date, Index, Integer, String, Table,
                        Text, create_engine)
from sqlalchemy_utils import  ChoiceType, create_database, database_exists

from datetime import datetime
try: 
    from config import POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER
except Exception:
    raise ImportError("Postgres config vars not found!")

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/test_task_db")

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    published = Column(String(50),nullable=False)
    beds = Column(String(50),nullable=False)
    price = Column(String(20), nullable=False)



def create_db_table(engine):
    if not database_exists(engine.url):
        create_database(engine.url)    
    if not engine.dialect.has_table(engine.connect(),table_name="posts"):
        Base.metadata.create_all(engine)
    
