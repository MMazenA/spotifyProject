from email import header
from flask import (
    Flask,
    render_template,
    Response,
    make_response,
    redirect,
    Request,
    request,
)
import requests
from flask_sse import sse
from flask_wtf.csrf import CSRFProtect
import time
import json


app = Flask(__name__)
csrf = CSRFProtect(app)


def get_time():
    """gives current time for stream"""
    time.sleep(1)
    s = time.ctime(time.time())
    return s


@app.route("/")
def root():
    r = make_response(render_template("index.html"))
    r.headers.set("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
    r.headers.setlist(
        "Content-Security-Policy",
        [
            "default-src 'self'; script-src 'sha256-F3mlFMaf/xZfaa9cAHii6pyBcI8dcn2MQSlm6GG+Vc0='; img-src https://i.scdn.co/; style-src 'self' 'unsafe-inline'"
        ],
    )

    r.headers.set("X-Content-Type-Options", "nosniff")
    r.headers.set("X-Content-Type-Options", "nosniff")
    r.headers.set("X-XSS-Protection", "1; mode=block")
    r.headers.set("X-Frame-Options", "SAMEORIGIN")
    r.headers.set("Access-Control-Allow-Methods", "GET")

    return r
    return render_template(
        "index.html",
        headers={
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "SAMEORIGIN",
            "X-XSS-Protection": "1; mode=block",
        },
    )


@app.route("/cat")
def bruh():
    r = make_response(render_template("cat.html"))
    r.headers.set("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
    r.headers.setlist(
        "Content-Security-Policy",
        [
            "default-src 'self'; script-src 'sha256-IRZbj3WeMT6hi8bYPB6DW7adQVdJYJfYBzhCPMQZEIg='; img-src https://purr.objects-us-east-1.dream.io/; connect-src https://aws.random.cat/meow"
        ],
    )

    r.headers.set("X-Content-Type-Options", "nosniff")
    r.headers.set("X-Content-Type-Options", "nosniff")
    r.headers.set("X-XSS-Protection", "1; mode=block")
    r.headers.set("X-Frame-Options", "SAMEORIGIN")
    r.headers.set("Access-Control-Allow-Methods", "GET")
    return r


@app.route("/stream")
def stream():
    def eventStream():
        fast_load = True
        while True:
            if fast_load:
                time.sleep(0.1)
            else:
                time.sleep(6)
            fast_load = False
            data = requests.get(
                "http://localhost:9888" + "/sptfy_server/", timeout=5
            ).json()["data"]
            # formating because requests.json was turning keys into single quotes
            data = "data: {}\n\n".format(json.dumps(data))
            # data = data.replace("'", '"')
            yield data

    return Response(
        eventStream(),
        mimetype="text/event-stream",
        headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src self",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "SAMEORIGIN",
            "X-XSS-Protection": "1; mode=block",
            "Access-Control-Allow-Methods": "GET",
        },
    )


@app.route("/stream2")
def stream2():
    def eventStream():
        fast_load = True
        while True:
            if fast_load:
                time.sleep(0.1)
            else:
                time.sleep(3600)
            fast_load = False
            data = requests.get(
                "http://localhost:9888/" + "/top_ten/", timeout=5
            ).json()
            # formating because requests.json was turning keys into single quotes
            data = "data: {}\n\n".format(json.dumps(data))
            # data = data.replace("'", '"')
            yield data

    return Response(
        eventStream(),
        mimetype="text/event-stream",
        headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src self",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "SAMEORIGIN",
            "X-XSS-Protection": "1; mode=block",
            "Access-Control-Allow-Methods": "GET",
        },
    )


@app.route("/callback/")
def callback():
    userauthenticate = (
        "response_type=code"
        + "&client_id="
        + "aa1826bc005040e98502bf7d9e6d5ba2"
        + "&scope=user-read-currently-playing%20user-read-playback-state%20user-read-playback-position"
        "&redirect_uri=https://mazenmirza.com/code/"
    )
    return redirect("https://accounts.spotify.com/authorize?" + userauthenticate)


@app.route("/code/")
def code():
    return request.args


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4443)