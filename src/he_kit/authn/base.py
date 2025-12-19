from abc import ABC, abstractmethod
from typing import Any, List, Optional

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field


class AuthContext(BaseModel):
    user_id: str
    tenants: List[str] = Field(default_factory=list)
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
    async def verify_token(self, token: str) -> AuthContext: ...

    @abstractmethod
    async def get_token(self, request: Request) -> str: ...

    @abstractmethod
    async def get_user(self, user_id: str) -> UserProfile: ...

    @abstractmethod
    async def get_users(self, user_ids: List[str]) -> List[UserProfile]: ...
