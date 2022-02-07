import sqlite3
from sqlite3 import Error
#from turtle import exitonclick


def create_table(conn, create_table_sql):
    c = conn.cursor()
    c.execute(create_table_sql)


def makeTable(name):
    database = f"{name}.db"

    sql_create_total_play_time = """
        CREATE TABLE IF NOT EXISTS total (
            song_id integer PRIMARY KEY,
            song_name text NOT NULL,
            artists text,
            primary_artist text,
            song_length text,
            lifetime_play_time text              
            ); """

    sql_create_current_tracker = """CREATE TABLE IF NOT EXISTS current (
            
            song_id integer PRIMARY KEY,
            song_name text NOT NULL,
            artists text,
            primary_artist text,
            song_length text,
            total_play_time text,
            current_play_time text,
            pic_link text text
            );"""

    conn = sqlite3.connect(database)

    create_table(conn, sql_create_total_play_time)
    create_table(conn, sql_create_current_tracker)
    print("plz")


makeTable("Table")
