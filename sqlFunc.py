"""Requires mysql and privateInfo for authentication."""
import mysql.connector
import privateinfo
import numpy as np


def data_insert(payload):
    """Insert data into mySQL database."""
    payload = list(payload.values())
    # inserting for update counts [x,playcount,playtime]
    payload = payload + list((payload[5],) + (payload[6],) + (payload[8],))

    sql = """INSERT INTO `current`
  (`song_id`, `song_name`, `artists`, `primary_artist`,
  `song_length`, `total_play_count`, `current_play_time`,
  `pic_link`,`rowid`)
   VALUES('%s',"%s","%s","%s",'%s','%s','%s',"%s","%s")
   ON DUPLICATE KEY UPDATE
  `total_play_count`='%s',
  `current_play_time`='%s',
  `rowid`='%s' """ % (
        tuple(payload)
    )
    try:
        mydb = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database=privateinfo.sql_db(),
            connection_timeout=5,
        )
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
            connection_timeout=5,
        )
        cur = mydb.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM `current` ORDER BY rowid DESC LIMIT 1"
            cur.execute(sql)
            row = cur.fetchone()
            cur.close()
            mydb.close()

        except mysql.connector.Error as err1:
            raise Exception("ERROR: Unable to retrive last row", err1) from err1

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
            connection_timeout=5,
        )
        mydb2 = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database=privateinfo.sql_db(),
            connection_timeout=5,
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
                `rowid`='%s'""" % (
                    row[0],
                    count,
                )
                cur_edit.execute(sql)
                mydb2.commit()
                count = count + 1
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
            connection_timeout=5,
        )
        cur = mydb.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM `current` WHERE `song_id`='%s'" % song_id
            cur.execute(sql)
            row = cur.fetchone()
            cur.close()
            mydb.close()

        except mysql.connector.Error as err1:
            raise Exception("ERROR: Unable to retrive requested row", err1) from err1

    except mysql.connector.Error as err:
        raise Exception("ERROR: Unable to connect to database", err) from err

    return row


def top_ten():
    """Get top 10 most played tracks."""
    row = ""
    try:

        mydb = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database=privateinfo.sql_db(),
            connection_timeout=5,
        )
        cur = mydb.cursor(dictionary=True, buffered=True)
        try:
            sql = "SELECT * FROM `current` ORDER BY `current`.`total_play_count` DESC LIMIT 10;"
            cur.execute(sql)
            row = cur.fetchall()
            cur.close()
            mydb.close()

            row = np.array(row)
            numbered_dict = dict(enumerate(row.flatten(), 1))

        except mysql.connector.Error as err1:
            raise Exception("ERROR: Unable to retrive requested row", err1) from err1

    except mysql.connector.Error as err:
        raise Exception("ERROR: Unable to connect to database", err) from err

    return numbered_dict


def add_user(id, display_name, refresh_token):
    """Create a new user in database."""

    sql = """INSERT INTO `users`
   (`id`, `display_name`, `refresh_token`)
   VALUES('%s',"%s","%s")
   ON DUPLICATE KEY UPDATE
  `id`='%s' """ % (
        tuple((id, display_name, refresh_token, id))
    )

    try:
        mydb = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database=privateinfo.sql_db(),
            connection_timeout=5,
        )
        cur = mydb.cursor()
        try:
            cur.execute(sql)
            mydb.commit()
            cur.close()
            mydb.close()
        except mysql.connector.Error as sqlerr1:
            print("Insert Error: Values: ", id, display_name, refresh_token, id)
            print(sqlerr1)
            print(sql)
            return False
    except mysql.connector.Error as sqlerr:
        print("Unable to connect to database: ", sqlerr)
        return False
    return True


def get_all_users():
    row = ""
    try:

        mydb = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database=privateinfo.sql_db(),
            connection_timeout=5,
        )
        cur = mydb.cursor(dictionary=True, buffered=True)
        try:
            sql = "SELECT * FROM `users`"
            cur.execute(sql)
            row = cur.fetchall()
            cur.close()
            mydb.close()

            row = np.array(row)
            print(row)
            numbered_dict = dict(enumerate(row.flatten(), 1))

        except mysql.connector.Error as err1:
            raise Exception("ERROR: Unable to retrive requested row", err1) from err1

    except mysql.connector.Error as err:
        raise Exception("ERROR: Unable to connect to database", err) from err

    return numbered_dict


def get_user_info(id):
    """Retrive specific user row from database."""
    row = ""
    try:

        mydb = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database=privateinfo.sql_db(),
            connection_timeout=5,
        )
        cur = mydb.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM `users` WHERE `id`='%s'" % id
            cur.execute(sql)
            row = cur.fetchone()
            cur.close()
            mydb.close()

        except mysql.connector.Error as err1:
            raise Exception("ERROR: Unable to retrive requested row", err1) from err1

    except mysql.connector.Error as err:
        raise Exception("ERROR: Unable to connect to database", err) from err
    return row


def make_table(id):
    """Create dynamic table based on ID. Does not overwrite pre-existing table"""
    row = ""
    try:

        mydb = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database=privateinfo.sql_db(),
            connection_timeout=5,
        )
        cur = mydb.cursor(dictionary=True)
        try:
            sql = (
                """CREATE TABLE IF NOT EXISTS  `%s` (
                    `song_id` varchar(50) NOT NULL,
                    `song_name` text NOT NULL,
                    `artists` text DEFAULT NULL,
                    `primary_artist` text DEFAULT NULL,
                    `song_length` text DEFAULT NULL,
                    `total_play_count` int(11) DEFAULT NULL,
                    `current_play_time` text DEFAULT NULL,
                    `pic_link` text DEFAULT NULL,
                    `date` datetime NOT NULL DEFAULT current_timestamp(),
                    PRIMARY KEY (`song_id`),
                    UNIQUE KEY `date`(`date`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
                % id
            )
            cur.execute(sql)
            cur.close()
            mydb.close()

        except mysql.connector.Error as err1:
            raise Exception("ERROR: Unable to retrive requested row", err1) from err1

    except mysql.connector.Error as err:
        raise Exception("ERROR: Unable to connect to database", err) from err
    return row


def insert_into_dynamic(id, payload):
    """Create dynamic table based on ID. Does not overwrite pre-existing table"""
    payload = list(payload.values())
    # payload.insert(0, id)
    # print(payload)
    # print(payload, len(payload))

    sql = """INSERT INTO {}
    (`song_id`, `song_name`, `artists`, `primary_artist`,
    `song_length`, `total_play_count`, `current_play_time`,
    `pic_link`)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """.format(
        id
    )

    try:
        mydb = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database=privateinfo.sql_db(),
            connection_timeout=5,
        )
        cur = mydb.cursor()
        try:
            cur.execute(sql, tuple(payload))
            mydb.commit()
            cur.close()
            mydb.close()
        except mysql.connector.Error as sqlerr1:
            print("Insert Error: Values: ", payload)
            print(sqlerr1)
            print(sql)
    except mysql.connector.Error as sqlerr:
        print("Unable to connect to database: ", sqlerr)


def get_last_week(id):
    """Retrive last week listening history based on ID"""

    row = ""
    try:

        mydb = mysql.connector.connect(
            host=privateinfo.sql_host(),
            user=privateinfo.sql_user(),
            password=privateinfo.sql_pass(),
            database=privateinfo.sql_db(),
            connection_timeout=5,
        )
        cur = mydb.cursor(dictionary=True, buffered=True)

        try:
            sql = """SELECT * 
                FROM `%s` 
                WHERE DATE_ADD(`date`, INTERVAL 7 DAY) >= NOW();""" % (
                id
            )
            cur.execute(sql)
            row = cur.fetchall()
            cur.close()
            mydb.close()

            rows = np.array(row)

        except mysql.connector.Error as err1:
            raise Exception("ERROR: Unable to retrive requested row", err1) from err1

    except mysql.connector.Error as err:
        raise Exception("ERROR: Unable to connect to database", err) from err

    return rows
