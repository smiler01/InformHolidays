# coding: utf-8
import os
import sys
import sqlite3
from datetime import datetime, date

class dateBaseProcessing:
    def __init__(self):
        self.dbPath = "./static/data/datebase.db"
        self.dayOfWeekList = ["日", "月", "火", "水", "木", "金", "土"]

    def getTodayDate(self):
        dateToday = datetime.strptime(datetime.now().strftime("%Y/%m/%d"), "%Y/%m/%d")
        return dateToday.timestamp()

    def getChainHolidays(self, numChain=3):
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        operation = "SELECT chaintag FROM datebase WHERE timestamp >= {};".format(self.getTodayDate())
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

        cursor.close()
        conn.close()
        return chainHolidayList

def main():
    dbp = dateBaseProcessing()
    dbp.getChainHolidays()

if __name__ == "__main__": main()