from fastapi_users.authentication import AuthenticationBackend

from app.core.authentication.transport import bearer_transport
from .strategy import get_jwt_strategy


authentication_backend = AuthenticationBackend(
    name="access-tokens-db",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)