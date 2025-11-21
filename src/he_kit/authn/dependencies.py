from fastapi import HTTPException, Request, status

from .base import AuthContext


def get_auth_context(request: Request) -> AuthContext:
    """Verify the request's Bearer token using the active auth backend and
    return the auth context.

    Raises HTTP 401 if the token is missing or invalid.

    """
    auth_provider = request.app.state.auth_provider
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
        )

    token = auth_header[len("Bearer ") :].strip()

    try:
        return auth_provider.verify_token(token)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
