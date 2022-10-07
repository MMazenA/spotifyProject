"""Requires mysql and privateInfo for authenticatio"""

import mysql.connector
import privateinfo


def data_insert(payload):
    """Inserts data into mySQL database."""
    # inserting for update counts [x,playcount,playtime]
    payload = payload+(payload[5],)+(payload[6],)+(payload[8],)
    sql = '''INSERT INTO `current` 
  (`song_id`, `song_name`, `artists`, `primary_artist`, `song_length`, `total_play_count`, `current_play_time`, `pic_link`,`rowid`) 
  VALUES('%s',"%s","%s","%s",'%s','%s','%s',"%s","%s") 
  ON DUPLICATE KEY UPDATE
  `total_play_count`='%s',
  `current_play_time`='%s',
  `rowid`='%s' ''' % (payload)
    try:
        mydb = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database="d"
        )
        cur = mydb.cursor()
    except:
        print("Unable to connect to database")
    try:
        cur.execute(sql)
        mydb.commit()
    except:
        print("Insert Error: Values: ", payload)
        print(sql)
    cur.close()
    mydb.close()


def last_row():
    row = ""
    try:
        mydb = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database="d"
        )
        cur = mydb.cursor()
    except:
        print("ERROR: Unable to connect to database")
    sql = "SELECT * FROM `current` ORDER BY rowid DESC LIMIT 1"

    try:
        cur.execute(sql)
        row = cur.fetchone()
        # print(row)

    except:
        print("ERROR: Unable to retrive last row")

    cur.close()
    mydb.close()
    return row


def reset_rows():
    """Clean up row count."""
    row = ""
    try:
        mydb = mysql.connector.connect(
            host=privateinfo.sqlHost(),
            user=privateinfo.sqlUser(),
            password=privateinfo.sqlPass(),
            database="d"
        )
        mydb2 = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
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

        while row is not None:
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
