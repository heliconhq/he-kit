from fastapi import Depends, Request
from fastapi.testclient import TestClient

from he_kit.authn.dependencies import get_auth_context
from he_kit.core.app import App
from he_kit.core.conf import DefaultSettings


def test_dummy_auth_adapter_valid_user():
    settings = DefaultSettings(AUTH_BACKEND="he_kit.authn.dummy.DummyAuthProvider")

    app = App(settings=settings)

    @app.get("/me")
    async def me(request: Request, auth=Depends(get_auth_context)):
        return {
            "user_id": auth.user_id,
            "tenant_id": auth.tenant_id,
        }

    client = TestClient(app)
    token = "tenant123:alice"
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()

    assert data["user_id"] == "alice"
    assert data["tenant_id"] == "tenant123"


def test_dummy_auth_adapter_invalid_header():
    settings = DefaultSettings(AUTH_BACKEND="he_kit.authn.dummy.DummyAuthProvider")

    app = App(settings=settings)

    @app.get("/me")
    async def me(request: Request, auth=Depends(get_auth_context)):
        return {
            "user_id": auth.user_id,
            "tenant_id": auth.tenant_id,
        }

    client = TestClient(app)
    token = "alice"
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
