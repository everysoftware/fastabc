from .db import DatabaseServerDsn, DatabaseDsn


class MysqlServerDsn(DatabaseServerDsn):
    dialect: str = "mysql"
    sync_driver: str = "mysql"
    async_driver: str = "aiomysql"


class MysqlDsn(MysqlServerDsn, DatabaseDsn):
    pass
