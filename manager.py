from threading import Thread
import time
import requests
import privateinfo
import single_tracker


def main():
    currently_tracking = []
    running_thread = []
    restart_timer = 60
    while True:
        users = requests.get(
            privateinfo.api_host() + "get_full_users/",
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=5,
        )
        if users.status_code != 200:
            time.sleep(restart_timer)
            continue

        for person in users.json()["data"]:
            if person["id"] not in currently_tracking:
                currently_tracking.append(person["id"])
                running_thread.append(
                    Thread(
                        target=single_tracker.main,
                        args=[person["refresh_token"], person["id"]],
                    )
                )
                running_thread[len(running_thread) - 1].start()

        for i, process in enumerate(running_thread):
            if not process.is_alive():
                print("Dead Thread Found, removing")
                del running_thread[i]
                del currently_tracking[i]
        time.sleep(restart_timer)


if __name__ == "__main__":
    main()
