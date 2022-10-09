"""
Modules used are listed below.

-----
base64
time
requests
"""
import base64
import time as t
import requests


class Sptfy:
    """A class to to be used in music tracking.

    Paramaters:
    --------
    Client ID
    Seceret ID
    Refresh Token

    Methods
    --------
    get_refresh_token
    get_access_token
    """

    def __init__(self, cid, sid, srt):
        """Class uses client id, secret id, and refresh token for all methods.

        Initialize takes (ClientID,SeceretID,ResfreshToken)
        """
        self.client_id = cid
        self.secret_id = sid
        self.refresh_token = srt
        self.token = 0

    def get_refresh_token(self, code):
        """Return refresh token given authurization code from OAuth2 URL."""
        token_url = "https://accounts.spotify.com/api/token"

        token_data_refresh = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://127.0.0.1:5000/home/"

        }
        client_creds = f"{self.client_id}:{self.secret_id}"
        client_creds_b64 = base64.b64encode(client_creds.encode())

        token_headers = {
            "Authorization": f"Basic {client_creds_b64.decode()}"
        }

        try:
            req_post = requests.post(token_url, data=token_data_refresh,
                                     headers=token_headers, timeout=5)
        except requests.exceptions.ConnectTimeout as err:
            print("get_refresh_token Error: Cannot connect \n", err)
            return 408
        resp_json = req_post.json()
        # print(resp_json)  # prints token ,type,scope
        requested_access_token = resp_json['access_token']
        return requested_access_token

    def get_access_token(self):
        """Return access token used to authenticate takes no parameters."""
        token_url = "https://accounts.spotify.com/api/token"

        token_data_refresh = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "redirect_uri": "http://127.0.0.1:5000/home/"
        }
        client_creds = f"{self.client_id}:{self.secret_id}"
        client_creds_b64 = base64.b64encode(client_creds.encode())

        token_headers = {
            "Authorization": f"Basic {client_creds_b64.decode()}"
        }

        try:
            req_post = requests.post(token_url, data=token_data_refresh,
                                     headers=token_headers, timeout=5)
        except requests.exceptions.ConnectTimeout as err:
            print("get_access_token Error: Cannot connect \n", err)
            return 408
        resp_json = req_post.json()
        requested_access_token = resp_json['access_token']
        return requested_access_token

    def get_current_track(self):
        """Return current listening track."""
        localt = t.localtime()
        time_string = t.strftime("<%m/%d/%Y, %H:%M:%S>", localt)

        if self.token == 0:
            self.token = self.get_access_token()

        current_track_url = 'https://api.spotify.com/v1/me/player'
        response = requests.get(
            current_track_url,
            headers={
                "Authorization": f"Bearer {self.token}"
            },
            timeout=5
        )

        # print()
        # print(time_string, response, end="")  # end="" to add db server or loal

        if response.status_code == 401:
            print("Authorization code expired retriving new token")
            self.token = self.get_access_token()
            return ["0", time_string, response]
        if response.status_code == 204:
            print("Connection made, Nothing is playing")
            return ['1', time_string, response]

        resp_json = response.json()

        if resp_json['currently_playing_type'] == 'track':
            artists = resp_json['item']['artists']
            current_track_info = {
                "id": resp_json['item']['id'],
                "name": resp_json['item']['name'],
                "artists": ', '.join([artist['name'] for artist in artists]),
                "position": resp_json['progress_ms'],
                "length": resp_json['item']["duration_ms"],
                "picture": resp_json['item']['album']['images'][0]['url'],
                "is_playing": resp_json['is_playing'],
                "main_artist": resp_json['item']['artists'][0]['name'],
            }
        else:
            return ['1', time_string, response]
        return [current_track_info, time_string, response]
