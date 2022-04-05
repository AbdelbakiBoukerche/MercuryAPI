from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Session:
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()
