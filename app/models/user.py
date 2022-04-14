import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, index=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    full_name = Column(Text, nullable=True)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )

    # Relationships
    user_role = relationship("UserRole", back_populates="user", uselist=False)

    def __repr__(self) -> str:
        return f"User: {self.username}"
