from urllib import request
import requests as req


payload = {
    "song_id": "6Xw3iWrQKgArwlRhVuU9CK",
    "song_name": "2SEATER (feat. Aaron Shaw, Samantha Nelson & Austin Feinstein)",
    "artisits": "Tyler, The Creator, Aaron Shaw, Samantha Nelson, Austin Feinstein",
    "primary_artist": "Tyler",
    "song_length": 217645,
    "total_play_count": 0,
    "current_play_time": "2000",
    "pic_link": "https://i.scdn.co/image/ab67616d0000b273e4bf0d3d9e0224a30ca5f665",
    "row_id": 351,
}

headers = {"Content-Type": "application/json; charset=utf-8"}


r = req.post("http://localhost:8080/sptfy_server/", headers=headers, json=payload)
print(r.status_code)
print(r.json())
