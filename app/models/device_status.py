from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class DeviceStatus(Base):

    __tablename__ = "device_status"

    id = Column(Integer, autoincrement=True, primary_key=True)

    timestamp = Column(DateTime)
    availability = Column(Boolean)
    response_time = Column(Integer)
    cpu = Column(Integer)
    memory = Column(Integer)

    # Relationships
    device_id = Column(Integer, ForeignKey("device.id"))
    device = relationship("Device", back_populates="device_statuses")

    def __repr__(self) -> str:
        return f"DeviceStatus: {self.device_id}"
