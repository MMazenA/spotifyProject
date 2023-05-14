"""Requires mysql and privateInfo for authentication. Singleton design pattern."""
import logging
import mysql.connector
import privateinfo
import db_connection as DBC

class SQL():
    """SQL queries handler."""
    def __init__(self) -> None:
        logger = logging.getLogger(__name__)
        log_format = "[%(asctime)s] [%(filename)s:%(lineno)s - %(funcName)15s() ] %(message)s"
        logging.basicConfig(filename='logs/sql.log', format=log_format, datefmt="%Y-%m-%d %H:%M:%S")
        logger.setLevel(logging.DEBUG)
        logger.debug('---Start---')
        self.conn = DBC.DBC(host=privateinfo.sql_host(),
                    user=privateinfo.sql_user(),
                    password=privateinfo.sql_pass(),
                    database=privateinfo.sql_db(),
                    connection_timeout=5,).get_connection()
        

        return {"data": row}

    def get_current_song(self,user_id):
        """Gets the current song someone is listening to given a user_id."""
        row = ""
        cur = self.conn.cursor(dictionary=True)
        try:
            sql = """
                SELECT song_id,song_name,artists,primary_artist,song_length,current_play_time,pic_link 
                FROM current_for_all 
                WHERE user_id=%s;
                """
            
            cur.execute(sql,(user_id,))
            row = cur.fetchone()
            cur.close()
        except mysql.connector.Error as err1:
            logging.debug(Exception("ERROR: Unable to retrive requested row", err1))
            raise Exception("ERROR: Unable to retrive requested row", err1) from err1

        return {"data": row}

    def get_top_four(self, user_id):
        """Returns top 4 plays for the week for a given user."""
        rows = ""
        sql = f"""
            SELECT song_id,song_name,pic_link, COUNT(*) AS count 
            FROM {user_id} 
            WHERE date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) 
            GROUP BY song_id 
            ORDER BY count DESC 
            LIMIT 4;
        """
        try: 
            cur = self.conn.cursor(dictionary=True)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()

        except mysql.connector.Error as err1:
            logging.debug(err1)
        
        numbered_rows = {}
        for i in enumerate(rows):
            numbered_rows[str(i[0]+1)] = rows[i[0]]
    
        return numbered_rows


    def get_all_users_safe(self):
        """Get user info besides sensitive information (keys)."""
        rows = ""
        
        cur = self.conn.cursor(dictionary=True, buffered=True)
        try:
            sql = "SELECT `id`,`display_name` FROM `users`"
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
        except mysql.connector.Error as err1:
            logging.debug(Exception("ERROR: Unable to retrive requested row", err1))
            raise Exception("ERROR: Unable to retrive requested row", err1) from err1
        
        return {"data": rows}
        
    def get_all_users(self):
        """Get all user information."""
        row = ""
        cur = self.conn.cursor(dictionary=True, buffered=True)
        try:
            sql = "SELECT * FROM `users`"
            cur.execute(sql)
            row = cur.fetchall()
            cur.close()
        except mysql.connector.Error as err1:
            logging.debug(Exception("ERROR: Unable to retrive requested row", err1))
            raise Exception("ERROR: Unable to retrive requested row", err1) from err1
        
        return {"data": row}

        






x =SQL()
print(x.get_current_song("eggzimic"))
print(x.get_top_four("eggzimic"))

    