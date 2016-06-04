import string
import sqlite3

class DBManager():
    def __init__(self):
        self._con = sqlite3.connect("mydatabaseS2.db3")
        self._con.text_factory = str
        self._cur = self._con.cursor()

    def getDBCur(self):
        return self._cur

    def getDBCon(self):
        return self._con