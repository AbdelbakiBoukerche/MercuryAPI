from sqlalchemy import Boolean, Column, Integer, Text


from app.db.base_class import Base


class Device(Base):

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    fqdn = Column(Text)
    serial_number = Column(Text)
    ip_address = Column(Text)
    mac_address = Column(Text)
    vendor = Column(Text)
    model = Column(Text)
    os = Column(Text)
    version = Column(Text)
    transport = Column(Text)

    availability = Column(Boolean)
    response_time = Column(Integer)
    sla_availability = Column(Integer, default=0)
    sla_response_time = Column(Integer, default=999)

    last_heard = Column(Text)

    cpu = Column(Integer)
    memory = Column(Integer)
    uptime = Column(Integer)

    os_compliance = Column(Boolean)
    config_compliance = Column(Boolean)
    last_compliance_check = Column(Text)

    ssh_port = Column(Integer)
    ncclient_name = Column(Text)
    netconft_port = Column(Integer)

    hostname = Column(Text)
    username = Column(Text)
    password = Column(Text)

    def __repr__(self) -> str:
        return f"Device: {self.name} - {self.hostname}"
