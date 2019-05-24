# coding: utf-8
import os
import datetime
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    today_datetime = datetime.date.today()
    return render_template("index.html", today_datetime=today_datetime)

if __name__ == "__main__":
    app.debug = True
    app.run()
