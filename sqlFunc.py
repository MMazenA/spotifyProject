
import mysql.connector
import privateInfo

def dataInsert(x):
  x=x+(x[5],)+(x[6],) #inserting for update counts [x,playcount,playtime]
  sql = '''INSERT INTO `current` 
  (`song_id`, `song_name`, `artists`, `primary_artist`, `song_length`, `total_play_count`, `current_play_time`, `pic_link`) 
  VALUES('%s',"%s","%s","%s",'%s','%s','%s',"%s") 
  ON DUPLICATE KEY UPDATE
  `total_play_count`='%s',
  `current_play_time`='%s' ''' %(x)
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
    print("Insert Error: Values: ",x)
  cur.close()
  mydb.close()


def lastRow():
  row=""
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
  sql="SELECT * FROM `current` ORDER BY rowid DESC LIMIT 1"

  try:
    cur.execute(sql)
    row = cur.fetchone()
  except:
    print("ERROR: Unable to retrive last row")

  cur.close()
  mydb.close()
  return row


