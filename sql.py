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

        if len(rows)<4:
            filler_row = {'song_id': 'NULL',
                          'song_name': '', 'artists': '',
                          'primary_artist': '',
                          'pic_link':
                          'https://i.scdn.co/image/ab67616d0000b2734c8974d1d37295694d7d4e8f',
                          'count': ''}
            iterations = 4 - len(rows)
            for i in range(iterations):
                rows.append(filler_row)

        numbered_rows = {}
        for i in enumerate(rows):
            numbered_rows[str(i[0]+1)] = rows[i[0]]
        return numbered_rows

    def get_user_info(self,user_id):
        """Retrive specific user row from database."""
        row = ""
        cur = self.conn.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM `users` WHERE `id`=%s"
            cur.execute(sql,(user_id,))
            row = cur.fetchone()
            cur.close()
        except mysql.connector.Error as err1:
            logging.debug(Exception("ERROR: Unable to retrive requested row", err1))
            raise Exception("ERROR: Unable to retrive requested row", err1) from err1
        return row

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
    

    def update_current_tracker(self,payload):
        """Updates the current song that someone is currently listening to."""
        user_id = payload[0]
        payload = list(payload[1].values())

        sql = """INSERT INTO `current_for_all`
        (`user_id`,`song_id`, `song_name`, `artists`, `primary_artist`,
        `song_length`, `current_play_time`,
        `pic_link`)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)  ON DUPLICATE KEY UPDATE
        `song_id`=%s,
        `song_name`=%s,
        `artists`=%s,
        `primary_artist`=%s,
        `song_length`=%s,
        `current_play_time`=%s,
        `pic_link`=%s"""

        val = (
            [user_id]+
            tuple(payload)+ 
            tuple(payload)
            )
   
        cur = self.conn.cursor()
        try:
            cur.execute(sql, val)
            self.conn.commit()
            cur.close()
        except mysql.connector.Error as sqlerr1:
            logging.debug("Insert Error: Values: ", payload,sqlerr1,sql)

    def insert_into_dynamic(self,id, payload):
        """Create dynamic table based on ID. Does not overwrite pre-existing table"""
        payload = list(payload.values())

        sql = """INSERT INTO {}
        (`song_id`, `song_name`, `artists`, `primary_artist`,
        `song_length`, `current_play_time`,
        `pic_link`)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """.format(
            id
        )
        cur = self.conn.cursor()
        try:
            cur.execute(sql, tuple(payload))
            self.conn.commit()
            cur.close()
        except mysql.connector.Error as sqlerr1:
            logging.debug("Insert Error: Values: ", payload,sqlerr1,sql)


    def make_current_tracker_table(self):
        """Create dynamic table based on ID. Does not overwrite pre-existing table"""
        cur = self.conn.cursor(dictionary=True)
        try:
            sql = """CREATE TABLE IF NOT EXISTS `current_for_all` (
                `user_id` varchar(200),
                `song_id` varchar(50) NOT NULL,
                `song_name` text NOT NULL,
                `artists` text DEFAULT NULL,
                `primary_artist` text DEFAULT NULL,
                `song_length` text DEFAULT NULL,
                `current_play_time` text DEFAULT NULL,
                `pic_link` text DEFAULT NULL,
                PRIMARY KEY (user_id),
                CONSTRAINT `user_id_lock`
                    FOREIGN KEY (user_id) REFERENCES users (id)
                    ON DELETE CASCADE
                    ON UPDATE RESTRICT
                
                ) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;"""
            cur.execute(sql)
            self.conn.commit()
            cur.close()
        except mysql.connector.Error as err1:
            logging.debug("ERROR: Unable to create current tracker table.", err1)

    def make_table(self,id):
        """Create dynamic table based on ID. Does not overwrite pre-existing table"""
        cur = self.conn.cursor(dictionary=True)
        try:
            sql = (
                """CREATE TABLE IF NOT EXISTS  `%s` (
                    `song_id` varchar(50) NOT NULL,
                    `song_name` text NOT NULL,
                    `artists` text DEFAULT NULL,
                    `primary_artist` text DEFAULT NULL,
                    `song_length` text DEFAULT NULL,
                    `current_play_time` text DEFAULT NULL,
                    `pic_link` text DEFAULT NULL,
                    `date` datetime NOT NULL DEFAULT current_timestamp(),
                    UNIQUE KEY `date`(`date`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
                % id
            )
            cur.execute(sql)
            self.conn.commit()
            cur.close()
        except mysql.connector.Error as err1:
            logging.debug("ERROR: Unable to create user table", err1)
            raise Exception("ERROR: Unable to create user table", err1) from err1




if __name__=="__main__":
    x =SQL()
    print(x.get_top_four("cizox_"))
    print(x.get_user_info("eggzimic"))



    