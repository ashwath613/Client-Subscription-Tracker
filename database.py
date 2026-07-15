from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# load the .env file
load_dotenv()

# get the cloud database fro neon database
DATABASE_URL = os.getenv("DATABASE_URL")

# enables the connection between the code and data bases
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# create the temporary workspace  or session for data mangement
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# covert the python class into database model
Base = declarative_base()

#dependency used for every requestion for database management
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()