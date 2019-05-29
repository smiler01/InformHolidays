# coding: utf-8
import os
import datetime
import sqlite3
from flask import Flask, render_template, request, redirect
#
from dateBase import dateBaseProcessing as dbp

app = Flask(__name__)

@app.route("/")
def index():
    todayDate = dbp().getTodayDate()
    chainHolidayList, numNextHolidaysList = dbp().getChainHolidays(numChain=3)
    return render_template("index.html", todayDate=todayDate[0], chainHolidayList=chainHolidayList,
                           numNextHolidaysList=numNextHolidaysList, numChain=3)

@app.route("/update", methods=["POST"])
def upload():
    if request.method == "POST": numChain = int(request.form["numChain"])
    else: numChain = 3
    todayDate = dbp().getTodayDate()
    chainHolidayList, numNextHolidaysList = dbp().getChainHolidays(numChain=numChain)
    return render_template("index.html", todayDate=todayDate[0], chainHolidayList=chainHolidayList,
                           numNextHolidaysList=numNextHolidaysList, numChain=numChain)

if __name__ == "__main__":
    app.debug = True
    app.run()
