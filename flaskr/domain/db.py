from flask import current_app, g
import pymysql
from pymysql.connections import Connection


def getDb() -> Connection:
    if not hasattr(g, 'db'):
        g.db = connectDb()
    if not g.db.open:
        g.db.connect()
    return g.db


def connectDb() -> None:
    return pymysql.connect(
        host=current_app.config['DB_HOSTNAME'],
        user=current_app.config['DB_USERNAME'],
        database=current_app.config['DB_NAME'],
        password=current_app.config['DB_PASSWORD'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


def _executeSqlFile(sqlfileName: str) -> None:
    sqls = ''
    with open('flaskr/resources/{}.sql'.format(sqlfileName)) as f:
        sqls = f.read()
    sqls = sqls.split(';')

    connection = getDb()
    with connection.cursor() as cursor:
        for sql in sqls:
            sql = sql.strip()
            if len(sql) > 0:
                cursor.execute(sql)

    connection.commit()


def destroyDb() -> None:
    _executeSqlFile('db_destroy')


def initDb() -> None:
    _executeSqlFile('db_init')


def closeDb():
    if hasattr(g, 'db') and g.db.open:
        g.db.close()
