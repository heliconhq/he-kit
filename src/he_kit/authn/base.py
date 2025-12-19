from abc import ABC, abstractmethod
from typing import Any, List, Optional

from fastapi import FastAPI, Request
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
    @classmethod
    @abstractmethod
    def setup(cls, app: FastAPI): ...

    @abstractmethod
    def verify_token(self, token: str) -> AuthContext: ...

    @abstractmethod
    def get_token(self, request: Request) -> str: ...

    @abstractmethod
    def get_user(self, user_id: str) -> UserProfile: ...

    @abstractmethod
    def get_users(self, user_ids: List[str]) -> List[UserProfile]: ...
