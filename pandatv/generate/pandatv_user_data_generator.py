import pymysql

db = pymysql.connect("localhost", "root", "1234", "pandatv")
cursor = db.cursor()


def get_insert_sql(user_id):
    return "insert into user values ({}, 'user')".format(user_id)


def insert(sql):
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


def close():
    db.close()


if __name__ == '__main__':
    for i in range(1, 999):
        insert(get_insert_sql(i))
    close()
