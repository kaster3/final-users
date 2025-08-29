from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader, HTTPBearer

from app.core.settings import settings

api_key_header = APIKeyHeader(name="X-API-Key")
http_bearer = HTTPBearer()

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True