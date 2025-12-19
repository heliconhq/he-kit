from fastapi import HTTPException, Request, status

from .base import AuthContext


def get_auth_context(request: Request) -> AuthContext:
    """Verify the request's Bearer token using the active auth backend and
    return the auth context.

    Raises HTTP 401 if the token is missing or invalid.

    """
    auth_provider = request.app.state.auth_provider

    token = auth_provider.get_token(request)

    try:
        return auth_provider.verify_token(token)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
