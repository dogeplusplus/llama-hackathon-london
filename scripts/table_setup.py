import os
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
from backend.tables import Base

load_dotenv(find_dotenv())

# Neon PostgreSQL connection string
DATABASE_URL = os.environ.get("POSTGRES_STR")
engine = create_engine(DATABASE_URL)

Base.metadata.drop_all(engine, checkfirst=True)
Base.metadata.create_all(engine, checkfirst=True)