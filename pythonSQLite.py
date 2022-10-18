"""Uses Sqlite3 to record data"""
import sqlite3


def create_table(conn, create_table_sql):
    """Create table if needed."""
    cur = conn.cursor()
    cur.execute(create_table_sql)


def make_table(name):
    """Create a table to insert listening data."""
    database = f"{name}.db"

    sql_create_current_tracker = """CREATE TABLE IF NOT EXISTS current (
            
            song_id text NOT NULL PRIMARY KEY,
            song_name text NOT NULL,
            artists text,
            primary_artist text,
            song_length text,
            total_play_count int,
            current_play_time text,
            pic_link text,
            rowid int
            );"""

    conn = sqlite3.connect(database, check_same_thread=False)

    create_table(conn, sql_create_current_tracker)


# makeTable("Table")


def data_insert(payload):
    """Inserts data into local database file using SQLite."""

    sql = """insert or replace into current(song_id,song_name,artists,primary_artist,
    song_length,total_play_count,current_play_time,pic_link,rowid)
    VALUES(?,?,?,?,?,?,?,?,?)
    """
    # conn = sqlite3.connect("Table.db")
    database = r"tracker.db"
    conn = sqlite3.connect(database, check_same_thread=False)

    with conn:

        # print(conn)
        cur = conn.cursor()
        cur.execute(sql, payload)
        conn.commit()
        # print(cur.lastrowid)
        return cur.lastrowid


def last_row():
    """Retrive and return last row from database."""
    database = r"tracker.db"
    conn = sqlite3.connect(database, check_same_thread=False)
    conn.row_factory = sqlite3.Row

    with conn:
        sql = """select *from current ORDER BY rowid DESC LIMIT 1"""
        cur = conn.cursor()
        cur.execute(sql)
        last_row_data = cur.fetchone()
        return dict(last_row_data)
