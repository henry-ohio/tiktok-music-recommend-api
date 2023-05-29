from typing import Any, Dict

from pydantic import BaseSettings, PostgresDsn, validator

"""
Settings for:
- Logging system
- Service name & Version
"""
from loguru import logger


class SQLSettings(BaseSettings):
    db_host: str = ''
    db_port: str = ''
    db_user: str = ''
    db_password: str = ''
    db_name: str = ''
    database_uri: PostgresDsn = None

    @validator('database_uri', pre=True)
    def assemble_db_connection(
        cls, value: str, values: Dict[str, Any],  # noqa: N805, WPS110
    ) -> str:
        if isinstance(value, str) and not value == '' and value is not None:
            return value

        return PostgresDsn.build(
            scheme='postgresql',
            user=values.get('db_user'),
            password=values.get('db_password'),
            host=values.get('db_host'),
            port=values.get('db_port'),
            path='/{0}'.format(values.get('db_name')),
        )
