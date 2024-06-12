from .db import DbServerDsn, DbDsn


class MysqlServerDsn(DbServerDsn):
    dialect: str = "mysql"
    sync_driver: str = "mysql"
    async_driver: str = "aiomysql"


class MysqlDsn(MysqlServerDsn, DbDsn):
    pass
