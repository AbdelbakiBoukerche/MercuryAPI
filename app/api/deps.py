from typing import Generator


from app.db.session import SessionLocal


# This will yield db Session for each request than closes it
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
