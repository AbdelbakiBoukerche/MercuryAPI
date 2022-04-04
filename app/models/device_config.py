from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class DeviceConfig(Base):
    __tablename__ = "device_config"

    id = Column(Integer, autoincrement=True, primary_key=True)

    timestamp = Column(DateTime)
    config = Column(Text)

    # Relationships
    device_id = Column(Integer, ForeignKey("device.id"))
    device = relationship("Device", back_populates="device_configs")

    def __repr__(self) -> str:
        return f"DeviceConfig: {self.device_id}"
