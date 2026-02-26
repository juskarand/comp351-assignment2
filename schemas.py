from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

SKU_REGEX = re.compile(r"^[A-Z0-9][A-Z0-9\-]{2,49}$") 

class ItemCreate(BaseModel):
    sku: str = Field(min_length=3, max_length=50)
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)

    quantity: int = Field(default=0, ge=0)
    unit_price: float = Field(default=0.0, ge=0)
    reorder_level: int = Field(default=0, ge=0)

    location: Optional[str] = Field(default=None, max_length=120)
    is_active: bool = True

    @field_validator("sku")
    @classmethod
    def sku_format(cls, v: str) -> str:
        v2 = v.strip().upper()
        if not SKU_REGEX.match(v2):
            raise ValueError("sku must be 3–50 chars, uppercase letters/digits, hyphen allowed (e.g., ABC-123)")
        return v2

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v2 = v.strip()
        if not v2:
            raise ValueError("name cannot be blank")
        return v2


class ItemUpdate(BaseModel):
    sku: Optional[str] = Field(default=None, min_length=3, max_length=50)
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)

    quantity: Optional[int] = Field(default=None, ge=0)
    unit_price: Optional[float] = Field(default=None, ge=0)
    reorder_level: Optional[int] = Field(default=None, ge=0)

    location: Optional[str] = Field(default=None, max_length=120)
    is_active: Optional[bool] = None

    @field_validator("sku")
    @classmethod
    def sku_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v2 = v.strip().upper()
        if not SKU_REGEX.match(v2):
            raise ValueError("sku must be 3–50 chars, uppercase letters/digits, hyphen allowed (e.g., ABC-123)")
        return v2

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v2 = v.strip()
        if not v2:
            raise ValueError("name cannot be blank")
        return v2


class ItemResponse(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str]
    quantity: int
    unit_price: float
    reorder_level: int
    location: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True
        