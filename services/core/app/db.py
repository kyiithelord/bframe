from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
from .models.base import Base
from .models import user, tenant, module

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
