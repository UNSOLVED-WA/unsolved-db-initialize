import sqlite3
import pymysql


def db_setting():
    db = pymysql.connect(
        user='root',
        passwd='990312aa',
        host='localhost',
        db='unsolved',
    )
    cur = db.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS problem('
                'id INTEGER PRIMARY KEY AUTO_INCREMENT,'
                'problem_number BIGINT,'
                'title VARCHAR(50),'
                'tier INTEGER,'
                'created_at DATETIME DEFAULT CURRENT_TIMESTAMP,'
                'updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP )')

    db.commit()
    cur.close()
    db.close()
