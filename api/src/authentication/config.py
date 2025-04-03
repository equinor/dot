import os
import requests
import uvicorn
from logging import getLogger
from pydantic import HttpUrl, ValidationError
from pydantic_settings import BaseSettings

logger = getLogger("uvicorn")

class AppSettings(BaseSettings):
    tenant_id: str
    aud: str
    issuer: HttpUrl
    jwks_uri: HttpUrl
    required_scope: list

def get_settings():
    try:
        app_settings = AppSettings(
            tenant_id = "3aa4a235-b6e2-48d5-9195-7fcf05b459b0",
            aud = "api://4251833c-b9c3-4013-afda-cbfd2cc50f3f",
            issuer ="https://sts.windows.net/3aa4a235-b6e2-48d5-9195-7fcf05b459b0/",
            jwks_uri = "https://login.microsoftonline.com/3aa4a235-b6e2-48d5-9195-7fcf05b459b0/discovery/v2.0/keys",
            required_scope= list(["Read",])
        )
    except ValidationError as exc:
        for err in exc.errors():
            logger.warning(f"{err['type']}: {', '.join(err['loc'])}")
        exit(1)
    return app_settings

def get_jwks(jwks_uri: str):
    return requests.get(jwks_uri).json()

def get_token_endpoint(well_known_conf_url: str):
    return requests.get(well_known_conf_url).json()["token_endpoint"]

def get_claims_options():
    config = get_settings()
    return {
        "iss": { "essential": True, "value": str(config.issuer) },  # Issuer must match config
        "aud": { "essential": True, "value": config.aud },  # Audience must match config
        "exp": { "essential": True  },  # EntraID token lifetime is 60-90min (75min on average)
        "nbf": { "essential": True },  
        "iat": { "essential": True },
        "scp": { "essential": True } 
    }