from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use your Neon PostgreSQL connection string
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_8HPbhwmGUN6t@ep-white-salad-a1dn62ah-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
