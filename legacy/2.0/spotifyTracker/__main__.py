#!/usr/bin/python3
"""Uses constant probing to identifty song changes and record them into databse via api."""
import time
import requests
import click
import sptfy
import privateinfo
import pythonSQLite


@click.command()
@click.option(
    "-l",
    "--local",
    metavar="BOOLEAN",
    help="Loal or server Output, defaults to server.",
)
def main(local):
    """Spotfiy tracker."""

    count_prevent = True
    if local is None:
        local = False
    else:
        local = True
    last_id = 0
    if local:
        pythonSQLite.make_table("tracker")
    sleep_timer = 25
    tracker = sptfy.Sptfy(
        privateinfo.client_id(), privateinfo.secret_id(), privateinfo.refresh_token()
    )

    while True:
        listining_info, time_string, response = tracker.get_current_track()
        if local:
            database = "<Local>"
        else:
            database = "<Server>"
        while listining_info == "408":
            print("Connection timeout, attempting to reconnect")
            time.sleep(30)
            listining_info, time_string, response = tracker.get_current_track()

        if listining_info == "1":
            print(time_string)
            print("Non-song type is currently playing")

        sleep_timer = 0
        if listining_info == "1":  # if current track is not a song
            sleep_timer = 29
        # pprint(listining_info, indent=4)
        if listining_info not in ("0", "1"):  # if data is available
            sleep_timer = 5
            if not listining_info.get("is_playing"):
                sleep_timer = 25
            repeat = True
            if local:
                last_song_db = requests.get(
                    privateinfo.api_host() + "/sptfy_local/", timeout=5
                ).json()
            else:
                last_song_db = requests.get(
                    privateinfo.api_host() + "/sptfy_server/", timeout=5
                ).json()["data"]

            if last_song_db is not None:
                last_id = last_song_db["song_id"]
                last_count = last_song_db["total_play_count"]
                last_row_id = last_song_db["rowid"]
            else:
                print("what does this do here")
                last_id = 0
                last_count = 0
                last_row_id = 0
            # count = 0
            if last_id != listining_info.get("id"):
                print()
                print(time_string, response, database)
                print(listining_info)
                print("different song playing now")
                locateSong = requests.get(
                    privateinfo.api_host()
                    + "/locate_song/"
                    + "?song_id="
                    + listining_info.get("id"),
                    headers={"Content-Type": "application/json; charset=utf-8"},
                    timeout=5,
                ).json()
                if locateSong is not None:
                    count = locateSong["total_play_count"]
                else:
                    count = 0

                count_prevent = True
            # accounts for songs on repeat
            if (
                last_id == listining_info.get("id")
                and not count_prevent
                and listining_info.get("position") < 30000
            ):
                count_prevent = True
                print("Repeating")
            if (
                last_id == listining_info.get("id")
                and listining_info.get("position") > 30000
                and count_prevent
            ):
                print("Adding 1 to count")
                count = int(last_count)
                count += 1
                count_prevent = False
                repeat = False
            elif last_id == listining_info.get("id") and repeat:
                count = last_count
            payload = {
                "song_id": str(listining_info.get("id")),
                "song_name": str(listining_info.get("name")),
                "artisits": str(listining_info.get("artists")),
                "primary_artist": str(listining_info.get("main_artist")),
                "song_length": str(listining_info.get("length")),
                "total_play_count": int(count),
                "current_play_time": str(listining_info.get("position")),
                "pic_link": str(listining_info.get("picture")),
            }

            if last_id != payload["song_id"]:
                last_row_id = last_row_id + 1
                # if last_row_id % 50 == 0 and not local:
                # sqlFunc.reset_rows()
            payload["row_id"] = last_row_id
            if local:
                requests.post(
                    privateinfo.api_host() + "/sptfy_local/",
                    headers={"Content-Type": "application/json; charset=utf-8"},
                    json=payload,
                    timeout=5,
                )
            else:
                # print(payload)
                requests.post(
                    privateinfo.api_host() + "/sptfy_server/",
                    headers={"Content-Type": "application/json; charset=utf-8"},
                    json=payload,
                    timeout=5,
                )
            # count = 0
        time.sleep(sleep_timer)


if __name__ == "__main__":
    main(False)
