from dynaconf import Dynaconf
from pydantic import AnyUrl
from pydantic_settings import BaseSettings


_settings = Dynaconf(
    settings_files=["config.yaml"]
)

_db_dsn = AnyUrl.build(
    scheme="postgresql+asyncpg",
    username=_settings.database.user,
    password=_settings.database.password,
    host=_settings.database.host,
    port=_settings.database.port,
    path=_settings.database.db,
)


class Settings(BaseSettings):
    db_dsn: str


settings = Settings(db_dsn=str(_db_dsn))
