from fastapi_users.authentication import JWTStrategy

from app.core.settings import settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.jwt_token.private_key.read_text(),
        lifetime_seconds=settings.jwt_token.lifetime_seconds,
        algorithm=settings.jwt_token.algorithm,
        public_key=settings.jwt_token.public_key.read_text(),
    )