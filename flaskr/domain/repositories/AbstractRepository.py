from pymysql.connections import Connection
from pymysql.err import DatabaseError


class AbstractRepository:
    def __init__(self, connection: Connection, table: str) -> None:
        self.connection = connection
        self.table = table

    def insertOne(self, contents: dict) -> int:
        values = list(contents.values())
        sql = "INSERT INTO `{}` (".format(self.table)
        sql += ",".join(contents.keys())
        sql += ") VALUES (" + ', '.join((['%s'] * len(values)))+");"

        id = None
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, values)
                id = cursor.lastrowid
        except DatabaseError as e:
            raise DBException(e)

        self.connection.commit()
        return id

    def findOneBy(self, params: dict) -> dict:
        sql = 'SELECT * FROM {}'.format(self.table)

        sql += self._getwhereBuilder(params)
        ret = None
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, list(params.values()))
                ret = cursor.fetchone()
        except DatabaseError as e:
            raise DBException(e)

        return ret

    def findOneRandom(self) -> dict:
        sql = 'SELECT * FROM {} ORDER BY RAND() LIMIT 1'.format(self.table)
        ret = None
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                ret = cursor.fetchone()
        except DatabaseError as e:
            raise DBException(e)

        return ret

    def findAllBy(self, params: dict) -> dict:
        sql = 'SELECT * FROM {}'.format(self.table)

        sql += self._getwhereBuilder(params)
        ret = None
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, list(params.values()))
                ret = cursor.fetchall()
        except DatabaseError as e:
            raise DBException(e)
        return ret

    def deleteBy(self, params: dict) -> int:
        sql = 'DELETE FROM {}'.format(self.table)

        sql += self._getwhereBuilder(params)

        ret = 0
        try:
            with self.connection.cursor() as cursor:
                ret = cursor.execute(sql, list(params.values()))
        except DatabaseError as e:
            raise DBException(e)
        return ret

    def _getwhereBuilder(self, params: dict) -> str:
        if len(params) > 0:
            where = " WHERE "
            tmp = list()
            for key in params.keys():
                tmp.append(key+"=%s")
            return where + " AND ".join(tmp)
        return ''


class DBException(Exception):
    def __init__(self, previous: Exception) -> None:
        self.previous = previous
