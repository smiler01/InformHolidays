#coding: utf-8
import os
import csv
from datetime import datetime, date
import sqlite3
import numpy as np
import pandas as pd

holidayDatetimeCSVPath = "../static/data/source/syukujitsu_modify.csv"

def getPublicHolidayDateData():
    df = pd.read_csv(holidayDatetimeCSVPath)
    timestamps  = [datetime.strptime(ds, "%Y/%m/%d").timestamp() for ds in df.datestring]
    datestrings = [datetime.strptime(ds, "%Y/%m/%d").strftime("%Y/%m/%d") for ds in df.datestring]
    dayOfWeekName = ["日", "月", "火", "水", "木", "金", "土"]
    dayofweeks  = [dayOfWeekName[datetime.strptime(ds, "%Y/%m/%d").weekday()] for ds in df.datestring]
    df["datestring"] = datestrings
    df["timestamp"] = timestamps
    df["dayofweek"] = dayofweeks
    df["type"] = "holiday"
    df = df.ix[:, [2, 0, 1, 3, 4]]
    return df

def getNormalHolidayDateData(startTimestamp, endTimestamp):
    normalHolidayDateData = []
    dayOfWeekName = ["日", "月", "火", "水", "木", "金", "土"]
    totalDateNum = int((endTimestamp - startTimestamp) / (60*60*24))
    for i in range(totalDateNum):
        targetTimestamp = i * (60*60*24) + startTimestamp
        targetDatetime = datetime.fromtimestamp(targetTimestamp)
        targetDate = targetDatetime.strftime("%Y/%m/%d")
        if (targetDatetime.weekday() == 0 or targetDatetime.weekday() == 6):
            normalHolidayDateData.append(
                [targetTimestamp, targetDate, "休日", dayOfWeekName[targetDatetime.weekday()], "normal"])
    df = pd.DataFrame(normalHolidayDateData, columns=['timestamp','datestring','name', 'dayofweek', 'type'])
    return df

def concatHolidayDateData(publicHolidayList, normalHolidayList):
    totalHolidayList = pd.concat([publicHolidayList, normalHolidayList])
    duplicatedHolidayList = totalHolidayList[totalHolidayList.duplicated(subset="timestamp", keep=False)] # 日にちが被る行を抽出
    duplicatedHolidayList = duplicatedHolidayList[duplicatedHolidayList.type != "normal"] # 通常の休日を削除（祝日を残す）
    totalHolidayList.drop_duplicates(subset="timestamp", inplace=True, keep=False) # 重複要素を一旦削除
    totalHolidayList = pd.concat([totalHolidayList, duplicatedHolidayList]) # 連結
    totalHolidayList.sort_values('timestamp', inplace=True) # timestamp順にソート
    totalHolidayList.reset_index(inplace=True, drop=True)
    return totalHolidayList

def tagChainHolidayDateData(totalHolidayDateData):
    dayOfWeekList = ["日", "月", "火", "水", "木", "金", "土"]
    chainHolidayiTagList = []
    chainNumber = 0
    for i in range(totalHolidayDateData.shape[0]):
        if i == 0:
            chainHolidayiTagList.append(0)
            continue
        preDayOfWeekIndex = dayOfWeekList.index(totalHolidayDateData.dayofweek[i-1])
        curDayOfWeekIndex = dayOfWeekList.index(totalHolidayDateData.dayofweek[i])
        if preDayOfWeekIndex == 6: preDayOfWeekIndex = -1
        if not (preDayOfWeekIndex + 1 == curDayOfWeekIndex): chainNumber += 1
        chainHolidayiTagList.append(chainNumber)
    totalHolidayDateData["chaintag"] = chainHolidayiTagList
    return totalHolidayDateData

def dfToSqlite(totalHolidayDateData):
    file_sqlite = "../static/data/datebase.db"
    conn = sqlite3.connect(file_sqlite)
    totalHolidayDateData.to_sql('datebase', conn, if_exists="append", index=None)
    conn.close()

def main():
    publicHolidayDateData = getPublicHolidayDateData()
    normalHolidayDateData = getNormalHolidayDateData(publicHolidayDateData.timestamp.values[0],
                                                     publicHolidayDateData.timestamp.values[-1])
    totalHolidayDateData  = concatHolidayDateData(publicHolidayDateData, normalHolidayDateData)
    totalHolidayDateData  = tagChainHolidayDateData(totalHolidayDateData)
    #print(totalHolidayDateData)
    dfToSqlite(totalHolidayDateData)

if __name__ == "__main__": main()