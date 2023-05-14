
import mysql.connector
import privateInfo


def dataInsert(x):
    # inserting for update counts [x,playcount,playtime]
    x = x+(x[5],)+(x[6],)+(x[8],)
    sql = '''INSERT INTO `current` 
  (`song_id`, `song_name`, `artists`, `primary_artist`, `song_length`, `total_play_count`, `current_play_time`, `pic_link`,`rowid`) 
  VALUES('%s',"%s","%s","%s",'%s','%s','%s',"%s","%s") 
  ON DUPLICATE KEY UPDATE
  `total_play_count`='%s',
  `current_play_time`='%s',
  `rowid`='%s' ''' % (x)
    try:
        mydb = mysql.connector.connect(
            host=privateInfo.sqlHost(),
            user=privateInfo.sqlUser(),
            password=privateInfo.sqlPass(),
            database="d"
        )
        cur = mydb.cursor()
    except:
        print("Unable to connect to database")
    try:
        cur.execute(sql)
        mydb.commit()
    except:
        print("Insert Error: Values: ", x)
        print(sql)
    cur.close()
    mydb.close()


def lastRow():
    row = ""
    try:
        mydb = mysql.connector.connect(
            host=privateInfo.sqlHost(),
            user=privateInfo.sqlUser(),
            password=privateInfo.sqlPass(),
            database="d"
        )
        cur = mydb.cursor()
    except:
        print("ERROR: Unable to connect to database")
    sql = "SELECT * FROM `current` ORDER BY rowid DESC LIMIT 1"

    try:
        cur.execute(sql)
        row = cur.fetchone()
        #print(row)

    except:
        print("ERROR: Unable to retrive last row")

    cur.close()
    mydb.close()
    return row


def resetRows():
    row = ""
    try:
        mydb = mysql.connector.connect(
            host=privateInfo.sqlHost(),
            user=privateInfo.sqlUser(),
            password=privateInfo.sqlPass(),
            database="d"
        )
        mydb2 = mysql.connector.connect(
            host=privateInfo.sqlHost(),
            user=privateInfo.sqlUser(),
            password=privateInfo.sqlPass(),
            database="d"
        )
        cur = mydb.cursor()
        curEdit = mydb2.cursor()
    except:
        print("ERROR: Unable to connect to database")
    sql = "SELECT * FROM `current` ORDER BY rowid ASC"

    try:
        cur.execute(sql)
        row = cur.fetchone()
        count = 0

        while(row != None):
            sql = """INSERT INTO `current` (`song_id`) VALUES ('%s') 
            ON DUPLICATE KEY UPDATE
            `rowid`='%s'""" % (row[0], count)
            curEdit.execute(sql)
            mydb2.commit()
            count = count+1
            row = cur.fetchone()

    except:
        print("Unable to resetRows")
        print(sql)

    cur.close()
    mydb.close()
    curEdit.close()
    mydb2.close()
