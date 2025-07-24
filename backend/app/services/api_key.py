from typing import List, Optional
from datetime import datetime
import secrets
from sqlalchemy.orm import Session

from app.models.api_key import APIKey
from app.schemas.api_key import APIKeyCreate, APIKeyUpdate

class APIKeyService:
    @staticmethod
    def get_api_keys(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[APIKey]:
        return (
            db.query(APIKey)
            .filter(APIKey.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create_api_key(db: Session, user_id: int, name: str) -> APIKey:
        api_key = APIKey(
            key=f"sk-{secrets.token_hex(32)}",
            name=name,
            user_id=user_id,
            is_active=True
        )
        db.add(api_key)
        db.commit()
        db.refresh(api_key)
        return api_key

    @staticmethod
    def get_api_key(db: Session, api_key_id: int) -> Optional[APIKey]:
        return db.query(APIKey).filter(APIKey.id == api_key_id).first()

    @staticmethod
    def get_api_key_by_key(db: Session, key: str) -> Optional[APIKey]:
        return db.query(APIKey).filter(APIKey.key == key).first()

    @staticmethod
    def update_api_key(db: Session, api_key: APIKey, update_data: APIKeyUpdate) -> APIKey:
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(api_key, field, value)
        db.add(api_key)
        db.commit()
        db.refresh(api_key)
        return api_key

    @staticmethod
    def delete_api_key(db: Session, api_key: APIKey) -> None:
        db.delete(api_key)
        db.commit()

    @staticmethod
    def update_last_used(db: Session, api_key: APIKey) -> APIKey:
        api_key.last_used_at = datetime.utcnow()
        db.add(api_key)
        db.commit()
        db.refresh(api_key)
        return api_key 