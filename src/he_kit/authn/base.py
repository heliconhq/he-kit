from abc import ABC, abstractmethod
from typing import Any, List, Optional

from pydantic import BaseModel


class AuthContext(BaseModel):
    user_id: str
    tenants: List[str] = []
    claims: dict[str, Any]
    auth_provider: str


class UserProfile(BaseModel):
    user_id: str
    name: str
    email: str
    photo_url: Optional[str] = None


class AuthProvider(ABC):
    @abstractmethod
    def verify_token(self, token: str) -> AuthContext:
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> UserProfile:
        pass

    @abstractmethod
    def get_users(self, user_ids: List[str]) -> List[UserProfile]:
        pass
