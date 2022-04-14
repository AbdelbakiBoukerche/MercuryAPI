from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True, nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), primary_key=True, nullable=False)

    # Relationships
    user = relationship("User", back_populates="user_role", uselist=False)
    role = relationship("Role")

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="unique_user_role"),)

    def __repr__(self) -> str:
        return f"UserRole: {self.user_id} - {self.role_id}"
