#coding: utf-8
import os
import csv
import datetime
import sqlite3
import numpy as np
import pandas as pd

holidayDatetimeCSVPath = "./static/data/syukujitsu_modify.csv"

def getPublicHolidayDateData():
    df = pd.read_csv(holidayDatetimeCSVPath)
    timestamp_list = \
        [datetime.datetime.strptime(date_str, "%Y/%m/%d").timestamp() for date_str in df.datestring]
    df["timestamp"] = timestamp_list
    df["type"] = "holiday"
    df = df.ix[:,[2, 0, 1, 3]]
    return df

def getNormalHolidayDateData(startTimestamp, endTimestamp):
    normalHolidayDateData = []
    dayOfWeekName = ["日", "月", "火", "水", "木", "金", "土"]
    totalDateNum = int((endTimestamp - startTimestamp) / (60*60*24))
    for i in range(totalDateNum):
        targetTimestamp = i * (60*60*24) + int(startTimestamp)
        targetDatetime = datetime.datetime.fromtimestamp(targetTimestamp)
        targetDate = targetDatetime.strftime("%Y/%m/%d")
        if (targetDatetime.weekday() == 0 or targetDatetime.weekday() == 6):
            normalHolidayDateData.append(
                [targetTimestamp, targetDate, dayOfWeekName[targetDatetime.weekday()], "normal"])
    df = pd.DataFrame(normalHolidayDateData, columns=['timestamp','datestring','name','type'])
    return df

def main():

    #print(datetime.date.today())
    publicHolidayDateData = getPublicHolidayDateData()
    normalHolidayDateData = getNormalHolidayDateData(publicHolidayDateData.timestamp.values[0],
                                                     publicHolidayDateData.timestamp.values[-1])
    print(normalHolidayDateData)

if __name__ == "__main__": main()