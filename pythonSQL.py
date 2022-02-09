import sqlite3
from sqlite3 import Error
#from tkinter import X

#from testSQL import create_connection
#from turtle import exitonclick


def create_table(conn, create_table_sql):
    c = conn.cursor()
    c.execute(create_table_sql)


def makeTable(name):
    database = f"{name}.db"

    sql_create_total_play_time = """
        CREATE TABLE IF NOT EXISTS total (
            song_id text PRIMARY KEY,
            song_name text NOT NULL,
            artists text,
            primary_artist text,
            song_length text,
            lifetime_play_time text              
            ); """

    sql_create_current_tracker = """CREATE TABLE IF NOT EXISTS current (
            
            song_id text PRIMARY KEY,
            song_name text NOT NULL,
            artists text,
            primary_artist text,
            song_length text,
            total_play_time text,
            current_play_time text,
            pic_link text
            );"""

    conn = sqlite3.connect(database)

    create_table(conn, sql_create_total_play_time)
    create_table(conn, sql_create_current_tracker)
    print("plz")


# makeTable("Table")

def dataInsert(x):
    # db="Table.db"

    sql = '''insert or replace into current(song_id,song_name,artists,primary_artist,
    song_length,total_play_time,current_play_time,pic_link)
    VALUES(?,?,?,?,?,?,?,?)
    '''
    #conn = sqlite3.connect("Table.db")
    database = r"Table.db"
    conn = sqlite3.connect(database)
    with conn:
        # print(conn)
        cur = conn.cursor()
        cur.execute(sql, x)
        conn.commit()
        # print(cur.lastrowid)
        return cur.lastrowid


makeTable("Table")
xx = 5400
y = 'XD'

xd = "(xx, y, 'mazen and me', 'me', '55', '52', '53', 'youtube.com')"
dataInsert((str(xx), y, 'XDDDDD', 'me', '55', '52', '53', 'youtube.com'))
#print((123, 'lol', 'mazen and me', 'me', '55', '52', '53', 'youtube.com'))
