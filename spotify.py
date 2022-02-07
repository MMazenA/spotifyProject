
from ast import Str
from os import access
from re import S
from urllib import response
import requests
from pprint import pprint
import base64
from urllib.parse import urlencode
import time
import privateInfo  # file containing client codes


def getAccessToken():
    client_id = privateInfo.clientID()
    secret_id = privateInfo.secretID()

    token_url = "https://accounts.spotify.com/api/token"

    token_data_refresh = {
        "grant_type": "refresh_token",
        "refresh_token": privateInfo.refreshToken(),
        "redirect_uri": "http://127.0.0.1:5000/home/"
    }
    client_creds = f"{client_id}:{secret_id}"
    client_creds_b64 = base64.b64encode(client_creds.encode())

    token_headers = {
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }

    r = requests.post(token_url, data=token_data_refresh,
                      headers=token_headers)
    resp_json = r.json()
    requested_access_token = resp_json['access_token']
    # print(r.json())
    # print(requested_access_token)
    # s_access_token=s_access_token= 'BQCsGhfymKzbYVXf_dP8M4OaUooU5DDQiS5Eqec7RPGGuBMBUxiqewQlWFKLS-8ygf4-4x1hBPkHvCIMmdQ_6GfJISdpbPOtSdUPSezFSxmOUvSkmD3ZcU8MZJhTC8kVAAE4zzxVCsVrZF6WHnYpkieoMw'

    return requested_access_token


def current_track(access_token):
    current_track_url = 'https://api.spotify.com/v1/me/player'
    response = requests.get(
        current_track_url,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    print(response)
    resp_json = response.json()
   # response = Str(response)
    # print(response.status_code)
    # print(type(response))
    global token
    # print(token)
    if(response.status_code != 200):

        token = getAccessToken()
        return 0

    if(resp_json['currently_playing_type'] == 'track'):
        track_id = resp_json['item']['id']
        track_name = resp_json['item']['name']
        artists = resp_json['item']['artists']
        main_artist = resp_json['item']['artists'][0]['name']
        artists_name = ', '.join([artist['name'] for artist in artists])
        time = [0, 0]
        position = resp_json['progress_ms']/1000
        time[0] = (int((position)/60))
        time[1] = (int((position) % 60))
        pic = resp_json['item']['album']['images'][0]['url']
        playing = resp_json['is_playing']
        length = [0, 0]
        length_raw = (resp_json['item']["duration_ms"])/1000
        length[0] = (int((length_raw)/60))
        length[1] = (int((length_raw) % 60))
        # percent_complete=f"% {position*100/length_raw}"
        current_track_info = {
            "id": track_id,
            "name": track_name,
            "artists": artists_name,
            "position": time,
            "length": length,
            "picture": pic,
            "is_playing": playing,
            "main_artist": main_artist,
            # "% complete":percent_complete
        }
    else:
        return 'Non-Track Playing?'
    return current_track_info


# print(getAccessToken())
def main():
    global token
    token = 0
    while(True):
        listining_info = current_track(token)
        # print(token)
        pprint(listining_info, indent=4)
        if(listining_info != 0):
            time.sleep(5)

        # sql stuff

    return listining_info


main()
