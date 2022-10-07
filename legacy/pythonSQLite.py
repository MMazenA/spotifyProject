import sqlite3


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
            
            song_id text NOT NULL PRIMARY KEY,
            song_name text NOT NULL,
            artists text,
            primary_artist text,
            song_length text,
            total_play_count int,
            current_play_time text,
            pic_link text
            );"""

    conn = sqlite3.connect(database, check_same_thread=False)

    create_table(conn, sql_create_total_play_time)
    create_table(conn, sql_create_current_tracker)
    print("plz")


# makeTable("Table")


def dataInsert(x):
    # db="Table.db"

    sql = '''insert or replace into current(song_id,song_name,artists,primary_artist,
    song_length,total_play_count,current_play_time,pic_link)
    VALUES(?,?,?,?,?,?,?,?)
    '''
    # conn = sqlite3.connect("Table.db")
    database = r"Table.db"
    conn = sqlite3.connect(database, check_same_thread=False)
    with conn:
        # print(conn)
        cur = conn.cursor()
        cur.execute(sql, x)
        conn.commit()
        # print(cur.lastrowid)
        return cur.lastrowid


def lastRow():
    database = r"Table.db"
    conn = sqlite3.connect(database, check_same_thread=False)
    with conn:
        sql = '''select *from current ORDER BY rowid DESC LIMIT 1'''
        cur = conn.cursor()
        last = cur.execute(sql)
        last_row = cur.fetchone()
        return last_row
