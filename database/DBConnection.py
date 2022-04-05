import pymysql


def databaseOperation(sqlQuery):
    db = pymysql.connect(host='localhost',
                             user='root',
                             password='mysql',
                             database='mifostenant',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    try:
        cursor.execute(sqlQuery)
        return cursor.fetchall()
    except Exception as e:
        raise ValueError(e)

    # disconnect from server
    db.close()


def databaseOperationSave(sqlQuery):
    db = pymysql.connect(host='localhost',
                             user='root',
                             password='mysql',
                             database='mifostenant',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    try:
        cursor.execute(sqlQuery)
        id = cursor.lastrowid
        db.commit()
        # return id
        # return cursor.fetchall()
    except:
        print("Error: unable to insert data")
        return False

    # disconnect from server
    db.close()
    return id