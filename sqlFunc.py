"""Requires mysql and privateInfo for authentication."""
import mysql.connector
import privateinfo


def data_insert(payload):
    """Insert data into mySQL database."""
    # inserting for update counts [x,playcount,playtime]
    payload = payload+(payload[5],)+(payload[6],)+(payload[8],)
    sql = '''INSERT INTO `current`
  (`song_id`, `song_name`, `artists`, `primary_artist`,
  `song_length`, `total_play_count`, `current_play_time`,
  `pic_link`,`rowid`)
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
            database=privateinfo.sql_db(),
            connection_timeout=5)
        cur = mydb.cursor()
        try:
            cur.execute(sql)
            mydb.commit()
            cur.close()
            mydb.close()
        except mysql.connector.Error as sqlerr1:
            print("Insert Error: Values: ", payload)
            print(sqlerr1)
            print(sql)
    except mysql.connector.Error as sqlerr:
        print("Unable to connect to database: ", sqlerr)


def last_row():
    """Retrive last row from database."""
    row = ""
    try:

        mydb = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database=privateinfo.sql_db(),
            connection_timeout=5
        )
        cur = mydb.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM `current` ORDER BY rowid DESC LIMIT 1"
            cur.execute(sql)
            row = cur.fetchone()
            cur.close()
            mydb.close()

        except mysql.connector.Error as err1:
            raise Exception(
                "ERROR: Unable to retrive last row", err1) from err1

    except mysql.connector.Error as err:
        raise Exception("ERROR: Unable to connect to database", err) from err

    return row


def reset_rows():
    """Clean up row count."""
    row = ""
    try:
        mydb = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database=privateinfo.sql_db(),
            connection_timeout=5
        )
        mydb2 = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database=privateinfo.sql_db(),
            connection_timeout=5
        )
        cur = mydb.cursor()
        cur_edit = mydb2.cursor()

        try:
            sql = "SELECT * FROM `current` ORDER BY rowid ASC"
            cur.execute(sql)
            row = cur.fetchone()
            count = 0

            while row is not None:
                sql = """INSERT INTO `current` (`song_id`) VALUES ('%s')
                ON DUPLICATE KEY UPDATE
                `rowid`='%s'""" % (row[0], count)
                cur_edit.execute(sql)
                mydb2.commit()
                count = count+1
                row = cur.fetchone()
                cur.close()
                mydb.close()
                cur_edit.close()
                mydb2.close()

        except mysql.connector.Error as err1:
            print("Unable to resetRows", err1)
            print(sql)
    except mysql.connector.Error as err:
        print("ERROR: Unable to connect to database", err)


def locate(song_id):
    """Retrive specific song id row from database."""
    row = ""
    try:

        mydb = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database=privateinfo.sql_db(),
            connection_timeout=5
        )
        cur = mydb.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM `current` WHERE `song_id`='%s'" % song_id
            cur.execute(sql)
            row = cur.fetchone()
            cur.close()
            mydb.close()

        except mysql.connector.Error as err1:
            raise Exception(
                "ERROR: Unable to retrive requested row", err1) from err1

    except mysql.connector.Error as err:
        raise Exception("ERROR: Unable to connect to database", err) from err

    return row
