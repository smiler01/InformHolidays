# coding: utf-8
import os
import sys
import sqlite3
from datetime import datetime, date

class dateBaseProcessing:
    def __init__(self):
        self.dbPath = "./static/data/datebase.db"
        self.dayOfWeekList = ["月", "火", "水", "木", "金", "土", "日"]

    def getTodayDate(self):
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        todayDate = datetime.strptime(datetime.now().strftime("%Y/%m/%d"), "%Y/%m/%d")
        #todayDate = datetime.strptime(("2019/06/03"), "%Y/%m/%d")
        operation = "SELECT * FROM datebase WHERE timestamp == {};".format(todayDate.timestamp())
        cursor.execute(operation)
        todayDateData = cursor.fetchall()
        if not todayDateData:
            todayDateData.append([
                todayDate.timestamp(),
                todayDate.strftime("%Y/%m/%d"),
                "平日",
                self.dayOfWeekList[todayDate.weekday()],
                "work",
            ])
        cursor.close()
        conn.close()
        return todayDateData

    def getChainHolidays(self, numChain=3):
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        todayTimestamp = datetime.strptime(datetime.now().strftime("%Y/%m/%d"), "%Y/%m/%d").timestamp()
        operation = "SELECT chaintag FROM datebase WHERE timestamp >= {};".format(todayTimestamp)
        cursor.execute(operation)
        chaintagList = cursor.fetchall()

        # /////
        chainHolidayList = []
        for tagNumber in range(chaintagList[0][0], chaintagList[-1][0]):
            operation = "SELECT * FROM datebase WHERE chaintag == {};".format(tagNumber)
            cursor.execute(operation)
            oneChainHolidayList = cursor.fetchall()
            if (len(oneChainHolidayList) >= numChain):
                chainHolidayList.append(oneChainHolidayList)

        # ////
        numNextHolidaysList = \
            [int((chainHoliday[0][0]-todayTimestamp)/(60*60*24)) for chainHoliday in chainHolidayList]

        cursor.close()
        conn.close()
        return chainHolidayList, numNextHolidaysList

def main():
    dbp = dateBaseProcessing()
    #a, b = dbp.getChainHolidays()
    #print(b)
    dbp.getTodayDate()

if __name__ == "__main__": main()