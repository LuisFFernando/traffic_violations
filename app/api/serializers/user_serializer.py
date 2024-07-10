import datetime
from email.policy import default
from pydantic import BaseModel, Field
from pydantic import field_validator
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, StringConstraints

from enum import Enum

from sqlalchemy import false


class CreateUserSerializer(BaseModel):
    name: str
    last_name: str
    nid: int
    address: str
    phone: str
    email: str


class UpdateUserSerializer(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class Order(str, Enum):
    asc = "ASC"
    desc = "DESC"


class ParamUserGetSerializer(BaseModel):
    """."""

    id: Optional[int] = None
    nid: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    active: bool = True


class UserDeserializer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    last_name: str
    nid: int
    address: str
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
