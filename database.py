from sqlalchemy.orm import sessionmaker

from database_services import get_engine_from_settings
from models import Base
from local_settings import postgresql as settings


# Creates connection to database
engine = get_engine_from_settings(settings)
print("Database connected successfully......")


# Add tables
Base.metadata.create_all(bind=engine)


# Creates session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
