from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "mysql+pymysql://root:123456@localhost/supply_chain_db"

engine = create_engine(DATABASE_URL)

Base = declarative_base()