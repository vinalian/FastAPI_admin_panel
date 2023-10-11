from pydantic import BaseModel, Field
from typing import Optional


__all__ = [
    'UserSchema',
    'ItemSchema',
]


class UserSchema(BaseModel):
    login: Optional[str] = Field(default=None, max_length=256)
    hashed_password: Optional[str] = Field(default=None, max_length=256)


class ItemSchema(BaseModel):
    name: Optional[str] = Field(default=None, max_length=256)
    user_id:  Optional[int] = Field(default=None, ge=-2147483648, gt=2147483647)


class UpdateAndDeleteItemSchema(BaseModel):
    id: str
    name: str
    user_id: str


class AppendSchema(BaseModel):
    name: str
    user_id: str
