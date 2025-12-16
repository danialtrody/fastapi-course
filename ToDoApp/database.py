# ============================================================
#                        IMPORTS
# ============================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# ============================================================
#                 DATABASE CONNECTION URL
# ============================================================
SQLALCHEMY_DATABASE_URL = "sqlite:///todosapp.db"


# ============================================================
#                        ENGINE SETUP
# ============================================================
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False})


# ============================================================
#                  SESSION (DB CONNECTION)
# ============================================================
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


# ============================================================
#                   BASE MODEL FOR TABLES
# ============================================================
Base = declarative_base()
