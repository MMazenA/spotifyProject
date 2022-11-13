#!/usr/bin/python3
"""Api for database interaction."""

from flask import Flask
from flask_restful import Api, Resource, reqparse, request

# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from flask_cors import CORS
import sqlFunc
import pythonSQLite


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


api.add_resource(SptfyServer, "/sptfy_server/")
api.add_resource(SptfyLocal, "/sptfy_local/")
api.add_resource(locateSong, "/locate_song/", endpoint="locate_song")
api.add_resource(top_ten, "/top_ten/", endpoint="top_ten")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=9888,
        debug=True,
        threaded=True,
    )
