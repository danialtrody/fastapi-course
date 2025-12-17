# ============================================================
#                           IMPORTS
# ============================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# ============================================================
#                    DATABASE CONFIGURATION
# ============================================================

# ------------------------------------------------------------
# SQLite (local development)
# ------------------------------------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///todosapp.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# ------------------------------------------------------------
# PostgreSQL (production / local postgres)
# ------------------------------------------------------------
# SQLALCHEMY_DATABASE_URL = (
#     "postgresql://postgres:123321@localhost:5432/TodoApplicationDatabase"
# )
#

# ============================================================
#                           ENGINE
# ============================================================
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# ============================================================
#                    SESSION (DB CONNECTION)
# ============================================================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================================
#                       BASE MODEL
# ============================================================
Base = declarative_base()
