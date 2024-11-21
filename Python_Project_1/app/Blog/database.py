from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the PostgreSQL URL (you can change the path or name of the database)
SQLALCHEMY_DATABASE_URL = "postgresql://momina:histo1969@localhost/fastapi_db"

# Create the engine to interact with the database (no need for check_same_thread for PostgreSQL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a base class for the models
Base = declarative_base()

# Create a session maker for handling sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
