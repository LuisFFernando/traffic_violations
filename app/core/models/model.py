from sqlalchemy import JSON, Column, Integer
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from config import postgres_conection
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import LargeBinary
from sqlalchemy import func


Base = postgres_conection.declarative_base()


class BaseModel(Base):
    __abstract__ = True

    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TrafficOfficer(BaseModel):
    __tablename__ = "traffic_officer"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    last_name = Column(Text)
    nid = Column(Integer, index=True, unique=True)
    address = Column(Text)

    phone = Column(Text)
    email = Column(Text, index=True, unique=True)
    password = Column(LargeBinary)

    violations = relationship("Violations", back_populates="traffic_officer")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return "<TrafficOfficer(id='%s', email='%s',nid='%s')>" % (self.id, self.email, self.nid)


class User(BaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    last_name = Column(Text)
    nid = Column(Integer, index=True, unique=True)
    address = Column(Text)

    phone = Column(Text)
    email = Column(Text, index=True, unique=True)

    vehicles = relationship("Vehicle", back_populates="user")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return "<User(id='%s', email='%s',nid='%s')>" % (self.id, self.email, self.nid)


class Vehicle(BaseModel):
    """."""

    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True)
    brand = Column(Text)
    model = Column(Text)
    color = Column(Text)
    serial = Column(Text, nullable=True, index=True, unique=True)
    description = Column(Text, nullable=True)
    placa_patente = Column(Text, nullable=False, unique=True)
    additional_data = Column(JSON, nullable=True)
    user_id = Column(Integer, ForeignKey(User.id))

    user = relationship("User", back_populates="vehicles")
    violations = relationship("Violations", back_populates="vehicles")

    def __repr__(self):
        return "<Vehicle(id='%s', serial='%s')>, placa_patente='%s'" % (self.id, self.serial, self.placa_patente)


class Violations(BaseModel):
    """."""

    __tablename__ = "violations"

    id = Column(Integer, primary_key=True)
    comentarios = Column(Text, nullable=False)
    placa_patente = Column(Text, nullable=False)
    additional_data = Column(JSON, nullable=True)
    timestamp = Column(Text, nullable=False)

    traffic_officer_id = Column(Integer, ForeignKey(TrafficOfficer.id))
    vehicle_id = Column(Integer, ForeignKey(Vehicle.id))

    vehicles = relationship("Vehicle", back_populates="violations")
    traffic_officer = relationship("TrafficOfficer", back_populates="violations")

    def __repr__(self):
        return "<Violations(id='%s', serial='%s')>, placa_patente='%s'" % (self.id, self.serial, self.placa_patente)
