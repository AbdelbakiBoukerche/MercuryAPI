from sqlalchemy import Column, Integer, Text

from app.db.base_class import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(Text, index=True)
    description = Column(Text)

    def __repr__(self) -> str:
        return f"Role: {self.name}"
