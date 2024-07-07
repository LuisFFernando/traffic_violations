import datetime
from email.policy import default
from pydantic import BaseModel, Field
from pydantic import field_validator
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, StringConstraints

from enum import Enum

from sqlalchemy import false


class LoginSerializer(BaseModel):
    email: str
    password: str


class CreateTrafficOfficerSerializer(BaseModel):
    name: str
    last_name: str
    nid: int
    phone: str
    email: str
    password: str


class UpdatedTrafficOfficerSerializer(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    nid: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class Order(str, Enum):
    asc = "ASC"
    desc = "DESC"


class ParamGetSerializer(BaseModel):
    """."""

    id: Optional[int] = None
    nid: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    active: bool = True


class ParamGetViolationsSerializer(BaseModel):
    """."""

    email: str


class TrafficOfficerDeserializer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    last_name: str
    nid: int
    phone: str
    email: str
    active: bool
    created_at: Optional[datetime.datetime] = ""
    updated_at: Optional[datetime.datetime] = ""

    @field_validator("created_at")
    def cast_created_at(cls, created_at):
        return str(created_at)

    @field_validator("updated_at")
    def cast_updated_at(cls, updated_at):
        return str(updated_at)


class CreateTrafficViolationsSerializer(BaseModel):
    """."""

    comentarios: str
    placa_patente: str
    additional_data: Optional[dict] = {}
    timestamp: str


class ViolationsDeserializer(BaseModel):
    """."""

    model_config = ConfigDict(from_attributes=True)
    comentarios: str
    placa_patente: str
    timestamp: str
    traffic_officer_id: int
    active: bool
    created_at: Optional[datetime.datetime] = ""
    updated_at: Optional[datetime.datetime] = ""

    @field_validator("created_at")
    def cast_created_at(cls, created_at):
        return str(created_at)

    @field_validator("updated_at")
    def cast_updated_at(cls, updated_at):
        return str(updated_at)


class VehicleViolationsDeserializer(BaseModel):
    """."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    brand: str
    model: str
    serial: str
    description: Optional[str]
    placa_patente: str
    color: Optional[str] = None

    violations: Optional[List[ViolationsDeserializer]]

    active: bool
    created_at: Optional[datetime.datetime] = ""
    updated_at: Optional[datetime.datetime] = ""

    @field_validator("created_at")
    def cast_created_at(cls, created_at):
        return str(created_at)

    @field_validator("updated_at")
    def cast_updated_at(cls, updated_at):
        return str(updated_at)
