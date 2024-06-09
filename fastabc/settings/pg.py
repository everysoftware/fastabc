from .db import DatabaseServerDsn, DatabaseDsn


class PgServerDsn(DatabaseServerDsn):
    dialect: str = "postgresql"
    sync_driver: str = "psycopg2"
    async_driver: str = "asyncpg"


class PostgresDsn(PgServerDsn, DatabaseDsn):
    pass
