from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class APIKeyBase(BaseModel):
    name: str
    is_active: bool = True

class APIKeyCreate(APIKeyBase):
    pass

class APIKeyUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

class APIKey(APIKeyBase):
    id: int
    key: str
    user_id: int
    last_used_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class APIKeyInDB(APIKey):
    pass 