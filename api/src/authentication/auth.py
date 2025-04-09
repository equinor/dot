import base64
import json
import logging
import time

from authlib.jose import JsonWebToken
from authlib.jose.errors import (
    InvalidClaimError,
    InvalidTokenError,
    UnsupportedAlgorithmError,
)
from fastapi import HTTPException, Request
from requests.exceptions import ConnectionError
from starlette.middleware.base import BaseHTTPMiddleware

from src.authentication.config import (
    get_claims_options,
    get_jwks,
    get_settings,
)

logger = logging.getLogger("uvicorn")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/"]:
            return await call_next(request)
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401, detail="Missing or invalid Authorization header"
            )
        token = auth_header.replace("Bearer ", "")
        try:
            config = get_settings()
            claims_options = get_claims_options()
            header = json.loads(base64.b64decode(token.split(".")[0]))
            logger.info(f"Verify token with header: {header}")
            logger.info(f"Claims options: {claims_options = }")

            jwt = JsonWebToken(["RS256"])  # Only allow RS256
            jwks = get_jwks(config.jwks_uri)
            claims = jwt.decode(token, jwks, claims_options=claims_options)
            claims.validate(now=time.time(), leeway=1)

            # Make sure one of the required scopes is present
            if not set(claims["scp"].split()).issubset(config.required_scope):
                logger.error(
                    f"One of the required scopes '{config.required_scope}' "
                    "is missing from token"
                )
                raise HTTPException(status_code=403, detail="Insufficient privileges")
            logger.info("Token verified OK")
            # Attach user info to request.state
            request.state.user = claims
            user = getattr(request.state, "user", None)
            if not user:
                raise HTTPException(
                    status_code=401, detail="Unauthorized: No user in request state"
                )
            roles = user.get("roles", [])
            if "DecisionOptimizationUser" not in roles:
                raise HTTPException(
                    status_code=403, detail="Forbidden: Insufficient role"
                )
            return await call_next(request)

        except ConnectionError as e:
            logger.error(f"Failed to get JWKS: {e}")
            raise HTTPException(status_code=500, detail="Failed to get JWKS")
        except (
            TypeError,
            InvalidClaimError,
            UnsupportedAlgorithmError,
            InvalidTokenError,
        ) as e:
            logger.error(f"Token validation failed: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
