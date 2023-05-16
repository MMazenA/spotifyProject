#!/usr/bin/python3
"""Uses constant probing to identifty song changes and record them into databse via api."""
import time
import requests
import sptfy
import privateinfo
import sqlFunc
import logging
import sql


def main(refresh_token, user_id):
    """Spotfiy tracker for single user and paramtized refresh token and user ID, saves only to server."""
    logger = logging.getLogger(__name__)
    log_format = "[%(asctime)s] [%(filename)s:%(lineno)s - %(funcName)15s()] %(message)s"
    logging.basicConfig(filename="logs/tracker.log", level=logging.INFO,format=log_format, datefmt="%Y-%m-%d %H:%M:%S")
    sql_func = sql.SQL()
    repeat_unlocked = True
    paused_time = 0
    last_id = 0
    tracker = sptfy.Sptfy(
        privateinfo.client_id(), privateinfo.secret_id(), refresh_token
    )

    while True:
        listining_info, time_string, response = tracker.get_current_track()
        while response == 408:
            logger.debug("Connection timeout, attempting to reconnect")
            time.sleep(30)
            listining_info, time_string, response = tracker.get_current_track()

        data_unavailable_codes=["0","1"]
        if listining_info not in data_unavailable_codes:  
            sleep_timer = 5
            payload = {
                "song_id": str(listining_info.get("id")),
                "song_name": str(listining_info.get("name")),
                "artisits": str(listining_info.get("artists")),
                "primary_artist": str(listining_info.get("main_artist")),
                "song_length": str(listining_info.get("length")),
                "current_play_time": str(listining_info.get("position")),
                "pic_link": str(listining_info.get("picture")),
            }
            if not bool(listining_info.get("is_playing")):
                paused_time += 4

            if listining_info.get("id") != last_id:  # if song is different
                logger.info([user_id,
                    time_string,
                    response,
                    "\ndifferent song streaming now\n",
                    listining_info]
                )
                last_id = listining_info.get("id")
                start_time = time.time()
                paused_time = 0
                repeat_unlocked = True
            else:  # if it is same song
                playing_for_25 = start_time + 25 + paused_time
                if playing_for_25 < time.time() and repeat_unlocked:
                    logger.info([user_id,time_string, response, "\nAdding 1 to count"])
                    repeat_unlocked = False
                    paused_time = 0
                    requests.post(
                        privateinfo.api_host() + "weekly_counter/{}".format(user_id),
                        headers={"Content-Type": "application/json; charset=utf-8"},
                        json=payload,
                        timeout=5,
                    )
                playing_for_55 = playing_for_25+30
                song_past_30= listining_info.get("position") < 30000
                if (
                    playing_for_55 < time.time()
                    and song_past_30
                ):  
                    start_time = time.time() + 5
                    repeat_unlocked = True
                    paused_time = 0
                    logger.info([user_id,"unlocked"])

                sql_func.update_current_tracker(list((user_id, payload)))

        else:
            sleep_timer = 29
        time.sleep(sleep_timer)


if __name__ == "__main__":
    main(privateinfo.refresh_token(), "eggzimic")
