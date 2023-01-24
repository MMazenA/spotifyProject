from threading import Thread
import time
import requests
import privateinfo
import single_tracker


def main():
    currently_tracking = set()
    running_thread = []
    while True:
        users = requests.get(
            privateinfo.api_host() + "get_full_users/",
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=5,
        )
        if users.status_code != 200:
            raise requests.exceptions.ConnectionError

        for person in users.json()["data"]:
            if person["id"] not in currently_tracking:
                currently_tracking.add(person["id"])
                running_thread.append(
                    Thread(
                        target=single_tracker.main,
                        args=[person["refresh_token"], person["id"]],
                    )
                )
                running_thread[len(running_thread) - 1].start() 

        for i,process in enumerate(running_thread):
            print("Dead Thread Found, removing")
            if not process.is_alive():
                running_thread.pop(i)
                currently_tracking.pop(i)
        time.sleep(10)


if __name__ == "__main__":
    main()
