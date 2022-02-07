from flask import Flask, redirect, url_for, render_template, request
import waitress

app = Flask(__name__)


@app.route("/")
def home():
    return (render_template("temp.html"))


@app.route("/admin/")
def admin():
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host='192.168.4.128', port="8000")
