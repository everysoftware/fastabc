from pydantic import SecretStr

from fastabc.settings import Dsn


class RedisDsn(Dsn):
    host: str
    port: int
    username: str = "default"
    password: SecretStr = SecretStr("")
    db: int = 0

    state_ttl: int | None = None
    data_ttl: int | None = None
