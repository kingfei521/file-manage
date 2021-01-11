import sqlite3
import os
from loguru import logger
DATABASE = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")), 'DB')
db = os.path.join(DATABASE, 'File.db')
import logging
def connet_db():
    return sqlite3.connect('/Users/kingfei/Desktop/FileUploadandDownload/DB/File.db')


def database(*args):
    conn = connet_db()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO tb_file (name, type, size, date ) VALUES (?, ?, ?, ?)""", (args))
    conn.commit()
    cursor.close()
    conn.close()


def query():
    conn = connet_db()
    cursor = conn.cursor()
    c = cursor.execute("""SELECT * FROM tb_file""")

    result = c.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    logger.debug('查询数据成功！')
    return result


def query_name(name):
    conn = connet_db()
    cursor = conn.cursor()

    sql = """SELECT *  FROM tb_file WHERE name='{}'""".format(name)
    c = cursor.execute(sql)

    one = c.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    logger.debug('查询数据成功！')
    return one

def update(date, name):
    conn = connet_db()
    cursor = conn.cursor()
    sql = """UPDATE tb_file SET date='{}' WHERE name='{}'""".format(date , name)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    logger.debug('更新数据成功！')


if __name__ == '__main__':
    query()