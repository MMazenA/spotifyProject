from flask import Flask, redirect, request
from urllib import request
from hyperlink import URL
import requests
import privateInfo   # file containing client codes


# client id and secret
client_id = privateInfo.clientID()
secret_id = privateInfo.secretID()


# authentication URL
userauthenticate = (
    "response_type=code" +
    '&client_id='+client_id +
    "&scope=user-read-currently-playing%20user-read-playback-state%20user-read-playback-position"
    "&redirect_uri=http://127.0.0.1:5000/home/"

)


# authentication using flask for browser
app = Flask(__name__)


def authenticate():

    @app.route("/")
    def spotify():
        return redirect('https://accounts.spotify.com/authorize?'+userauthenticate)

    @app.route("/home/")
    def home():
        return ('hi')

    app.run(host='0.0.0.0')


authenticate()
