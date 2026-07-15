from sqlalchemy import create_engine
from database import Base, DATABASE_URL, engine
import models


def main():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    main()
