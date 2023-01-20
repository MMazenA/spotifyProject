from email import header
from flask import (
    Flask,
    render_template,
    Response,
    make_response,
    redirect,
    Request,
    request,
    session,
    url_for,
)
import requests
from flask_sse import sse
from flask_wtf.csrf import CSRFProtect
import time
import json
import datetime
import os


app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = os.urandom(24)
expire_date = datetime.datetime.now()
expire_date = expire_date + datetime.timedelta(days=30)


def get_time():
    """gives current time for stream"""
    time.sleep(1)
    s = time.ctime(time.time())
    return s


def verify_user():
    cookies = getCookies()[0]
    if cookies.get("logged_in") == True:
        return True


def getCookies():
    userID = request.cookies.get("userID")
    displayUser = request.cookies.get("displayUser")
    logged_in = request.cookies.get("logged_in")
    code = request.cookies.get("code")
    if userID is None:
        userID = ""
    if displayUser is None:
        displayUser = ""
    if logged_in is None:
        logged_in = ""
    # if code is None:
    #     logged_in = ""
    return [
        {
            "id": userID,
            "display_name": displayUser,
            "logged_in": logged_in,
            "code": code,
        }
    ]


@app.route("/")
def root():

    data = getCookies()

    r = make_response(render_template("index.html", data=data))
    r.headers.set("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
    # r.headers.setlist('Content-Security-Policy', [
    #     "default-src 'self'; script-src 'sha256-F3mlFMaf/xZfaa9cAHii6pyBcI8dcn2MQSlm6GG+Vc0='; img-src https://i.scdn.co/; style-src 'self' 'unsafe-inline'"])

    r.headers.set("X-Content-Type-Options", "nosniff")
    r.headers.set("X-XSS-Protection", "1; mode=block")
    r.headers.set("X-Frame-Options", "SAMEORIGIN")
    r.headers.set("Access-Control-Allow-Methods", "GET")

    return r


@app.route("/cat/")
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
    r.headers.set("X-XSS-Protection", "1; mode=block")
    r.headers.set("X-Frame-Options", "SAMEORIGIN")
    r.headers.set("Access-Control-Allow-Methods", "GET")
    return r


@app.route("/stream/<id>/")
def stream(id):
    def eventStream():
        try:
            fast_load = True
            while True:
                if fast_load:
                    time.sleep(0.1)
                else:
                    time.sleep(6)
                fast_load = False
                data = requests.get(
                    "http://localhost:9888" + "/get_current_song/" + id, timeout=5
                ).json()["data"]
                # formating because requests.json was turning keys into single quotes
                data = "data: {}\n\n".format(json.dumps(data))
                # data = data.replace("'", '"')
                yield data
        finally:
            print("Client disconnected stream1")

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


@app.route("/stream2/<id>/")
def stream2(id):
    def eventStream():
        try:
            fast_load = True
            while True:
                if fast_load:
                    time.sleep(0.1)
                else:
                    time.sleep(3600)
                fast_load = False
                data = requests.get(
                    "http://localhost:9888/" + "/get_top_four/" + id, timeout=5
                ).json()
                # formating because requests.json was turning keys into single quotes
                data = "data: {}\n\n".format(json.dumps(data))
                # print(data)
                yield data
        finally:
            print("Client disconnected stream1")

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
    if request.referrer == "https://mazenmirza.com/confirm/":
        userauthenticate = (
            "response_type=code"
            + "&client_id="
            + "aa1826bc005040e98502bf7d9e6d5ba2"
            + "&scope=user-read-currently-playing%20user-read-playback-state%20user-read-playback-position%20user-read-private"
            "&redirect_uri=https://mazenmirza.com/code/"
        )
        return redirect("https://accounts.spotify.com/authorize?" + userauthenticate)
    resp = make_response(redirect(url_for("confirm")))

    for key, value in getCookies():
        resp.set_cookie(key, value)
    return resp


@app.route("/code/")
def code():
    data = requests.post(
        "http://localhost:9888" + "/NewUser/?code=" + request.args["code"], timeout=5
    )

    r = redirect(url_for("userInfo"))
    r.set_cookie("displayUser", data.json()["display_name"], expires=expire_date)
    r.set_cookie("userID", data.json()["id"], expires=expire_date)
    r.set_cookie(
        "code",
        request.args["code"],
        expires=datetime.datetime.now() + datetime.timedelta(minutes=60),
    )
    if (
        data.json()["id"] == ""
        or data.json()["id"] == None
        or data.json()["display_name"] == ""
        or data.json()["display_name"] == None
    ):
        r.set_cookie("logged_in", "False", expires=expire_date)
    else:
        r.set_cookie("logged_in", "True", expires=expire_date)

    return r


@app.route("/UserInfo/")
def userInfo():
    data = getCookies()
    if [(x) for x in data[0].values() if x == "" or x == None]:
        resp = make_response(render_template("accessDenied.html", data=data))
        resp.set_cookie("userID", "", expires=1)
        resp.set_cookie("displayUser", "", expires=1)
        resp.set_cookie("logged_in", "False", expires=expire_date)

        return resp

    r = make_response(render_template("userInfo.html", data=data))
    return r


@app.route("/log_out/")
def log_out():
    resp = redirect(url_for("root"))
    resp.set_cookie("userID", "", expires=1)
    resp.set_cookie("displayUser", "", expires=1)
    resp.set_cookie("logged_in", "False", expires=expire_date)

    return resp


@app.route("/User/<user>/")
def user(user):
    data = requests.get("http://localhost:9888" + "/allusers/", timeout=5).json()[
        "data"
    ]
    cookies_data = getCookies()
    for person in data:
        if user == person.get("id"):
            r = make_response(render_template("tracker.html", data=cookies_data))
            return r

    return make_response(render_template("userNotFound.html", data=cookies_data))

    return {"name": user}


@app.route("/Users/")
def users():
    data = getCookies()[0]

    data.update(
        {
            "names": requests.get(
                "http://localhost:9888" + "/allusers/", timeout=5
            ).json()["data"]
        }
    )
    print(data)

    r = make_response(render_template("users.html", data=[data]))
    return r


@app.route("/about/")
def about():
    return redirect("https://github.com/MMazenA/spotifyProject")


@app.route("/confirm/")
def confirm():
    cookies_data = getCookies()
    r = make_response(render_template("confirm.html", data=cookies_data))
    return r


@app.errorhandler(403)
@app.route("/forbidden/")
def forbidden():
    cookies_data = getCookies()
    r = make_response(render_template("accessDenied.html", data=cookies_data))
    return r, 403


@app.errorhandler(404)
def not_found(e):
    cookies_data = getCookies()
    return make_response(render_template("404.html", data=cookies_data)), 404


@app.errorhandler(500)
def not_found(e):
    cookies_data = getCookies()
    return make_response(render_template("500.html", data=cookies_data)), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4443)
