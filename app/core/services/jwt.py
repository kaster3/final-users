import jwt

from app.core import Settings


class JWTHelper:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_user_id(self, token) -> int:
        token = token.replace("Bearer ", "")
        payload = jwt.decode(
            token,
            self.settings.jwt_token.public_key.read_text(),
            algorithms=self.settings.jwt_token.algorithm
        )
        user_id = payload.get("sub")
        return int(user_id)