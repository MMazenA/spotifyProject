"""Uses time and sql or sqlite3. """
import time
import sqlFunc
import sptfy
import privateinfo
import pythonSQLite


def main():
    """spotfiy tracker."""
    count_prevent = True
    local = False
    if local:
        pythonSQLite.create_table("tracker")
    sleep_timer = 25
    tracker = sptfy.Sptfy(privateinfo.client_id(),
                          privateinfo.secret_id(),
                          privateinfo.refresh_token())

    while True:
        listining_info = tracker.get_current_track()
        print(listining_info)
        sleep_timer = 0
        if listining_info == 1:
            sleep_timer = 29
        # pprint(listining_info, indent=4)
        if listining_info not in (0, 1):  # if data is available
            sleep_timer = 5
            if not listining_info.get('is_playing'):
                sleep_timer = 25
            repeat = True
            if local:
                last_song_db = pythonSQLite.last_row()
            else:
                last_song_db = sqlFunc.last_row()
            if last_song_db is not None:
                last_id = last_song_db[0]
                last_count = last_song_db[5]
                last_row_id = last_song_db[8]
            else:
                last_id = 0
                last_count = 0
                last_row_id = 0
            count = 0
            if last_id != listining_info.get('id'):
                print("different song playing now")
                count_prevent = True
            # accounts for songs on repeat
            if (last_id == listining_info.get('id') and
                    not count_prevent and
                    listining_info.get('position') < 30000):
                count_prevent = True
                print('Repeating')
            if (last_id == listining_info.get('id') and
                listining_info.get('position') > 30000 and
                    count_prevent):
                print("Adding 1 to count")
                count = int(last_count)
                count += 1
                count_prevent = False
                repeat = False
            elif(last_id == listining_info.get('id') and repeat):
                count = last_count
            payload = (str(listining_info.get('id')),
                       str(listining_info.get('name')),
                       str(listining_info.get('artists')),
                       str(listining_info.get('main_artist')),
                       str(listining_info.get('length')),
                       int(count),
                       str(listining_info.get('position')),
                       str(listining_info.get('picture')))
            # print(payload)
            if last_id != payload[0]:
                last_row_id = last_row_id+1
                if last_row_id % 50 == 0 and not local:
                    sqlFunc.reset_rows()
            payload = payload+(last_row_id,)
            # print("LAST ROW: ", last_row_id)
            if local:
                pythonSQLite.data_insert((payload))
            sqlFunc.data_insert((payload))
            # count = 0
        time.sleep(sleep_timer)


if __name__ == "__main__":
    main()
