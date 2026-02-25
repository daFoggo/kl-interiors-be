from pydantic import BaseModel, EmailStr, ConfigDict, Field, model_validator, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: str
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None

    @field_validator('email', 'phone_number', mode='before')
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str = Field(min_length=6)
    
    @model_validator(mode='after')
    def check_email_or_phone(self) -> 'UserCreate':
        if not self.email and not self.phone_number:
            raise ValueError('Either email or phone number is required')
        return self

class UserResponse(UserBase):
    id: UUID
    role: RoleEnum
    is_active: bool
    created_at: datetime
    updated_at: datetime
