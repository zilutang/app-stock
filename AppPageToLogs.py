import urllib2
import time
import string
from sgmllib import SGMLParser
from EastmoneyContent import *
from DBManager import *
from URLBuilder import *
import os
import lxml.html.soupparser as soupparser
import csv

import sys
reload(sys)
sys.setdefaultencoding('gbk')


class LogManager(SGMLParser):
    def __init__(self):
        self._fileSet = set()
        self._path ="K:\\codes\\ApplicationStock\\ApplicationStocks\\sh"
        self._csvfile = open('holders.csv', 'ab')
    def getFileSet(self):

        os.chdir(self._path)

        if len(self._fileSet) == 0:
            for root, dirs, files in os.walk( self._path ):
                for fn in files:
                    self._fileSet.add(root + "\\" + fn)


    def generateALine(self, file):
        fileobj = open(file)
        lineTmp = []
        print(file[-6:])
        print("\n")
        
        try:
            dom = soupparser.fromstring(fileobj)
            nameTmp = dom.body.xpath('//div[@class="qphox"]//div[@class="sckifbox"]//div[@class="scklox"]//div[@class="cnt"]//text()')[2].replace(' ', '')[1:]

            
            self._csvfile.write(file[-6:])  #add ID

            self._csvfile.write(',')
            self._csvfile.write(nameTmp)    #add Name

            count = 0
            for ele in dom.body.xpath('//table[@id="Table0"]//th[@class="tips-dataL"]'):
                txt = ele.text

                count += 1
                self._csvfile.write(',')
                self._csvfile.write(txt)    #add Date
            

            if count < 10:
                for i in range(0, 10 - count):
                     self._csvfile.write(',')

            countColum = count
            count = 0

            for ele in dom.body.xpath('//table[@id="Table0"]//td[@class="tips-dataL"]'):
                count += 1
                txt = ele.text
                txtTmp = txt[-1:]
                if txtTmp == u'\u4e07':
                    iTmp = float(txt[:-1]) * 10000
                    txt = str(iTmp)
                    pass

                self._csvfile.write(',')
                self._csvfile.write(txt)    #add data

                if count == countColum:
                    for i in range(0, 10 - count):
                        self._csvfile.write(',')
                    count = 0
                    pass

            self._csvfile.write('\n')
            fileobj.close()
        except:
            pass

    def generateLog(self):
        self.getFileSet()
        #self._fileSet.add(self._path + "\\300260")
        i = 0
        for ele in self._fileSet:
            i += 1
            print(i)            
            self.generateALine(ele)
        self._csvfile.close()
        pass


LogInstance = LogManager();
LogInstance.generateLog()