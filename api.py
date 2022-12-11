#!/usr/bin/python3
"""Api for database interaction."""

import base64
import json
from flask import Flask
from flask_restful import Api, Resource, reqparse, request
import requests


# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from flask_cors import CORS
import sqlFunc
import pythonSQLite
import privateinfo
import sptfy


app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

song_post_args = reqparse.RequestParser()
song_post_args.add_argument("song_id", type=str, help="Song data")
song_post_args.add_argument("song_name", type=str, help="Song data")
song_post_args.add_argument("artisits", type=str, help="Song data")
song_post_args.add_argument("primary_artist", type=str, help="Song data")
song_post_args.add_argument("song_length", type=str, help="Song data")
song_post_args.add_argument("total_play_count", type=int, help="Song data")
song_post_args.add_argument("current_play_time", type=str, help="Song data")
song_post_args.add_argument("pic_link", type=str, help="Song data")
song_post_args.add_argument("row_id", type=int, help="Row ID")


insert_post_args = reqparse.RequestParser()
insert_post_args.add_argument("song_id", type=str, help="Song data")
insert_post_args.add_argument("song_name", type=str, help="Song data")
insert_post_args.add_argument("artisits", type=str, help="Song data")
insert_post_args.add_argument("primary_artist", type=str, help="Song data")
insert_post_args.add_argument("song_length", type=str, help="Song data")
insert_post_args.add_argument("total_play_count", type=int, help="Song data")
insert_post_args.add_argument("current_play_time", type=str, help="Song data")
insert_post_args.add_argument("pic_link", type=str, help="Song data")
insert_post_args.add_argument("row_id", type=int, help="Row ID")


class SptfyServer(Resource):
    """Spotify Server endpoint for insertion and retrival."""

    def get(self):
        """Method to return data from cloud sql database."""
        return {"data": sqlFunc.last_row()}

    def post(self):
        """Method to insert into sql database"""
        args = song_post_args.parse_args()

        sqlFunc.data_insert(args)
        return {"Status": "Sucess"}


class weekly_counter(Resource):
    def post(self, user_id):
        print(user_id)
        args = insert_post_args.parse_args()
        args.pop("row_id", None)
        sqlFunc.insert_into_dynamic(user_id, args)

    def get(self, user_id):
        return sqlFunc.get_last_week(user_id)


class locateSong(Resource):
    """Spotify Server endpoint for locating a specific song."""

    def get(self):
        """Method to return data from cloud sql database."""
        args = request.args
        return sqlFunc.locate(args["song_id"])


class top_ten(Resource):
    """End point that returns top 10 most listened to songs."""

    def get(self):
        """Method to return data from cloud sql database."""
        return sqlFunc.top_ten()


class SptfyLocal(Resource):
    """Spotify Local endpoint for insertion and retrival."""

    def get(self):
        """Method to return last row from local database."""
        return pythonSQLite.last_row()

    def post(self):
        """Method to insert into local database."""

        args = song_post_args.parse_args()
        pythonSQLite.data_insert(args)
        return {"Status": "Sucess"}


class NewUser(Resource):
    """Endpoint for new users to create an account"""

    def post(self):
        token_url = "https://accounts.spotify.com/api/token"
        token_data_code = {
            "grant_type": "authorization_code",
            "code": request.args["code"],
            "redirect_uri": "https://mazenmirza.com/code/",
        }
        client_creds = f"{privateinfo.client_id()}:{privateinfo.secret_id()}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        token_headers = {"Authorization": f"Basic {client_creds_b64.decode()}"}
        try:
            req_post = requests.post(
                token_url,
                data=token_data_code,
                headers=token_headers,
                timeout=5,
                verify=True,
            )
            token = req_post.json()["access_token"]
            refresh_token = req_post.json()["refresh_token"]
            # print("1: ", req_post, req_post.json())
            # print("token: ", token)

        except:
            return {"Status": "408"}

        try:
            response = requests.get(
                "https://api.spotify.com/v1/me",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                },
                timeout=5,
                verify=True,
            )
            # print(response)
            if response.status_code == 403:
                return {"display_name": "", "id": ""}

            if response.status_code != 200:
                return {"display_name": "", "id": ""}
            if response.status_code == 200:
                self.add_user(
                    response.json()["id"],
                    response.json()["display_name"],
                    refresh_token,
                )
                return response.json()
            else:
                return 408
        except requests.exceptions.ReadTimeout as timeout:
            return 408
        except requests.exceptions.ConnectionError as err:
            print("Error: Cannot connect \n", err)
            return 408

    def add_user(self, id, display_name, refresh_token):
        if sqlFunc.add_user(id, display_name, refresh_token):

            return 200
        else:
            return 400


class get_user(Resource):
    def get(self, id):
        return sqlFunc.get_user_info(id)


api.add_resource(SptfyServer, "/sptfy_server/")
api.add_resource(SptfyLocal, "/sptfy_local/")
api.add_resource(locateSong, "/locate_song/", endpoint="locate_song")
api.add_resource(top_ten, "/top_ten/", endpoint="top_ten")
api.add_resource(NewUser, "/NewUser/", endpoint="NewUser")
api.add_resource(get_user, "/user/<id>", endpoint="user")
api.add_resource(weekly_counter, "/weekly_counter/<user_id>", endpoint="weekly_counter")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=9888,
        debug=True,
        threaded=True,
    )
