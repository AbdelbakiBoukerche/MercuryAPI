from sqlalchemy.orm import Session

from app.core.logger import logger

from app.db.base import Base
from app.db.session import engine


def init_db(db: Session) -> None:
    logger.debug("Initializing Database...")

    Base.metadata.create_all(bind=engine)
