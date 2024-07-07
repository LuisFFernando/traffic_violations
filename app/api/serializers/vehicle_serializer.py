import datetime
from email.policy import default
from pydantic import BaseModel, Field
from pydantic import field_validator
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, StringConstraints

from enum import Enum

from sqlalchemy import false


class CreateVehicleSerializer(BaseModel):
    brand: str
    model: str
    serial: str
    description: Optional[str]
    placa_patente: str
    color: str

    additional_data: Optional[dict] = {}


class UpdateVehicleSerializer(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    serial: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    placa_patente: Optional[str] = None
    additional_data: Optional[dict] = {}


class ParamVehicleGetSerializer(BaseModel):
    """."""

    id: Optional[int] = None
    placa_patente: Optional[int] = None
    active: bool = True


class VehicleDeserializer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    brand: str
    model: str
    serial: str
    description: Optional[str]
    placa_patente: str
    color: Optional[str] = None

    additional_data: Optional[dict] = {}
    user_id: int
    active: bool
    created_at: Optional[datetime.datetime] = ""
    updated_at: Optional[datetime.datetime] = ""

    @field_validator("created_at")
    def cast_created_at(cls, created_at):
        return str(created_at)

    @field_validator("updated_at")
    def cast_updated_at(cls, updated_at):
        return str(updated_at)
