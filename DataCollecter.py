import urllib2
import time
import string
from sgmllib import SGMLParser
from EastmoneyContent import *
from DBManager import *
from URLBuilder import *
import os
class DataCollecter():
    def __init__(self):
        self._DBHandle = DBManager()
        self._DBCur = self._DBHandle.getDBCur()
        self._DBCon = self._DBHandle.getDBCon()
        self._URLInstance = URLBuilder()
        self._code = ""
        self._Component = ""
        self._fileSet = set()
        pass

    def UpdateStocks(self, mark, IDHead, IDTail):
        try:
            self._DBCur.execute('''CREATE TABLE collections ''' + '''
                             (code text, recordtype text, date text, holders real, holderschangeper real, averagehold real, averageholdchangeper real, 
                             scr text, price real, averageamount real, top10hold real, top10outstandinghold real)''')
        except:
            pass

        countTmp = 0
        for x in range(IDHead,IDTail):
            urlToGet = self._URLInstance.GetURL(self.BuildCode(mark, x, 1))
            try:
                content = urllib2.urlopen(urlToGet).read()
                time.sleep(3)
                countTmp += 1
                if countTmp == 50:
                    time.sleep(6)
                    countTmp = 0
            except:
                continue
            
            self._ContentInstance = EastmoneyContent()
            self._ContentInstance.feed(content)

            self._ContentInstance.handle_listmatrix(self.BuildCode(mark, x, 0), "F10")

            #-----------------begin sqlite----------------------------
            if self._ContentInstance.listmatrix != []:
                
                for iteminlistmatrix in self._ContentInstance.listmatrix:
                    codeTmp = iteminlistmatrix[0]
                    dateTmp = iteminlistmatrix[2]
                    executeSQL = 'select * from collections where date = \"' + dateTmp + '\" and code = \"' + codeTmp + '\"'
                
                    self._DBCur.execute(executeSQL)
                    
                    SQLTmp = self._DBCur.fetchall()
                    if  SQLTmp == []:
                        executeSQL = 'INSERT INTO collections VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'    
                        self._DBCur.execute(executeSQL, iteminlistmatrix)
                        self._DBCon.commit()

                print " done\n"
                self._DBCon.commit()
            else:
                print "  has none\n"


    def BuildCode(self, mark, x, mix):
        if mark == "sh":
            self._code = "6" + str(x)[-5:]
            self._Component = mark + self._code
        if mark == "sz":
            self._code = str(x)[-6:]
            self._Component = mark + self._code

        if mix == 1:
            return self._Component
        if mix == 0:
            return self._code

    def UpdateStockname(self, filename):
        x = 0
        for line in open(filename):
            if x == 0 : 
                x += 1
                continue
            x += 1
            linesplited = line.split('\t')
            executeSQL = '  update collections set name = \"' + linesplited[2] + '\" where code = ' + linesplited[1] + '  '
            self._DBCur.execute(executeSQL)
            self._DBCon.commit()
            pass

    def NewTab(self, filename):
        x = 0
        
        for line in open(filename):
            firstline = []
            pricenow = []
            if x == 0 : 
                x += 1
                firstline = line.split('\t')
                try:
                    self._DBCur.execute('''CREATE TABLE price ''' + '''(code text, newprice real, toplevel real, toplimitdays real)''')
                except:
                    pass

                continue

            x += 1
            linesplited = line.split('\t')
            executeSQL = 'INSERT INTO price VALUES (?,?,?,?)'              
            pricenow.append(linesplited[1][1:7])  
            pricenow.append(linesplited[7])
            pricenow.append(linesplited[10])
            pricenow.append(linesplited[8])
            self._DBCur.execute(executeSQL, pricenow)
            self._DBCon.commit()
            pass

    def UpdateStocksHtmls(self, mark, IDList):
        countTmp = 0
        #if not os.path.isdir(mark):
        #   os.makedirs(mark)
        path = "K:\\codes\\ApplicationStock\\ApplicationStocks\\sh"
        os.chdir(path)

        if len(self._fileSet) == 0:
            for root, dirs, files in os.walk( path ):
                for fn in files:
                    self._fileSet.add(fn)

        for x in IDList:
            '''
            for root, dirs, files in os.walk( path ):
                for fn in files:
                    if fn not in self._fileSet:
                        self._fileSet.add(fn)
            '''
            
            urlToGet = self._URLInstance.GetURL(self.BuildCode(mark, x, 1))
            if urlToGet[-6:] in self._fileSet:
                continue
            
            if os.path.exists(urlToGet[-6:]) == True:
                continue
            try:
                content = urllib2.urlopen(urlToGet).read()
                time.sleep(1)
                countTmp += 1
                if countTmp == 50:
                    time.sleep(6)
                    countTmp = 0
            except:
                continue

            fileobj = open(urlToGet[-6:], "wb")
            fileobj.write(content)
            fileobj.close()

    def UpdateStocksHtmlsFinance(self, mark, IDHead, IDTail):
        countTmp = 0
        if not os.path.isdir(mark + "finance"):
           os.makedirs(mark + "finance")

        os.chdir( "./" + mark + "finance" + "/")
        for x in range(IDHead,IDTail):
            urlToGet = self._URLInstance.GetURL(self.BuildCode(mark, x, 1))
            try:
                content = urllib2.urlopen(urlToGet).read()
                time.sleep(0)
                countTmp += 1
                if countTmp == 50:
                    time.sleep(6)
                    countTmp = 0
            except:
                continue

            fileobj = open(urlToGet[-8:], "wb")
            fileobj.write(content)
            fileobj.close()
           