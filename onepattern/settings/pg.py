from .db import DbServerDsn, DbDsn


class PgServerDsn(DbServerDsn):
    dialect: str = "postgresql"
    sync_driver: str = "psycopg2"
    async_driver: str = "asyncpg"


class PostgresDsn(PgServerDsn, DbDsn):
    pass
