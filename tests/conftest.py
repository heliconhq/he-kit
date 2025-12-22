from typing import Dict

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from keycloak import KeycloakOpenID


@pytest.fixture(scope="session")
def keycloak_token() -> Dict[str, str]:
    kc = KeycloakOpenID(
        server_url="http://localhost:8080",
        realm_name="teron",
        client_id="teron-core-api",
        client_secret_key="tjWtEoiKhGl7mH8nkg3s2DUGnugJjwQA",
    )

    token = kc.token(
        username="demo",
        password="demo",
    )

    return token


@pytest.fixture
def kc_client(keycloak_token):
    client = APIClient()

    access_token = keycloak_token["access_token"]
    claims = jwt.get_unverified_claims(access_token)

    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
    client.user_id = claims["sub"]

    return client
