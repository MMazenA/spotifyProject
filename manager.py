from threading import Thread
import requests
import privateinfo
import single_tracker


def main():
    currently_tracking = set()
    running_thread = []
    while True:

        users = requests.get(
            privateinfo.api_host() + "allusers/",
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
                        target=single_tracker.main(
                            person["refresh_token"], person["id"]
                        )
                    )
                )
                running_thread[len(running_thread) - 1].start()  # starting the thread


if __name__ == "__main__":
    main()
