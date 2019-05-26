# coding: utf-8
import os
import datetime
import sqlite3
from flask import Flask, render_template, request, redirect
#
from dateBase import dateBaseProcessing

app = Flask(__name__)

@app.route("/")
def index():
    chainHolidayList = dateBaseProcessing().getChainHolidays()
    return render_template("index.html", chainHolidayList=chainHolidayList)

if __name__ == "__main__":
    app.debug = True
    app.run()
