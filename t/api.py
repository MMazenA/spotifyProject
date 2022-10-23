#!/usr/bin/python3
from flask import Flask
import sqlFunc
import pythonSQLite
from flask_restful import Api, Resource, reqparse
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS, cross_origin


app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
# limiter = Limiter(app, key_func=get_remote_address)


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


class sptfy_server(Resource):
    # decorators = [limiter.limit("60/minute")]

    def get(self):
        return {"data": sqlFunc.last_row()}

    def post(self):
        args = song_post_args.parse_args()

        sqlFunc.data_insert(args)
        return {"Status": "Sucess"}


class sptfy_local(Resource):
    def get(self):
        return pythonSQLite.last_row()

    def post(self):
        args = song_post_args.parse_args()

        pythonSQLite.data_insert(args)
        return {"Status": "Sucess"}


api.add_resource(sptfy_server, "/sptfy_server/")
api.add_resource(sptfy_local, "/sptfy_local/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
