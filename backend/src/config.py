"""
Contains all the configuration variables used thoughout the application.
These parameters have the intention that they can be changed/modified at runtime to provide deployment configuration.
Specifically the SECRET_KEY parameter can be generated and changed with each run so it is not the same each time.
"""
# pylint: disable=too-few-public-methods
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Settings for Rosalution.  See https://fastapi.tiangolo.com/advanced/settings/
    for more details.
    """
    api_base_url: str = "http://dev.cgds.uab.edu/rosalution/api"
    web_base_url: str = "http://dev.cgds.uab.edu/rosalution"
    mongodb_host: str = "rosalution-db"
    mongodb_db: str = "rosalution_db"
    rosalution_key: str
    auth_web_failure_redirect_route = "/login"
    oauth2_access_token_expire_minutes: int = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days
    oauth2_algorithm: str = "HS256"
    openapi_api_token_route: str = "/auth/token"
    cas_api_service_url: str = "http://dev.cgds.uab.edu/rosalution/api/auth/login?nexturl=%2F"
    cas_server_url: str = "https://padlockdev.idm.uab.edu/cas/"
    cas_login_enable: bool = False


@lru_cache()
def get_settings():
    """
    Returns the instance of initializing the settings.  Utilizing lru_cache caches the result so that it is only
    reading from the environment variables once for the settings, instead of multiple times.
    """
    return Settings()
