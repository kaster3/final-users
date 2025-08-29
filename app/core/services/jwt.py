import jwt
from fastapi import HTTPException, status

from app.core import Settings


class JWTHelper:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_user_id(self, token) -> int:
        token = token.replace("Bearer ", "")
        try:
            payload = jwt.decode(
                token,
                self.settings.jwt_token.public_key.read_text(),
                algorithms=self.settings.jwt_token.algorithm,
                options={"verify_aud": False},
            )
        except jwt.exceptions.InvalidSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid auth token",
            )
        user_id = payload.get("sub")
        return int(user_id)


