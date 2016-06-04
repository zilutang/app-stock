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

MaxCount = 5

class LogManager(SGMLParser):
    def __init__(self):
        self._fileSet = set()
        self._path ="K:\\codes\\ApplicationStock\\ApplicationStocks\\sh"
        self._csvfile = open('holdersSdltgd.csv', 'ab')
    def getFileSet(self):

        os.chdir(self._path)

        if len(self._fileSet) == 0:
            for root, dirs, files in os.walk( self._path ):
                for fn in files:
                    self._fileSet.add(root + "\\" + fn)


    def generateALine(self, file):
        fileobj = open(file)        
        lineTmp = []
        dom = soupparser.fromstring(fileobj)
        try:
            nameTmp = dom.body.xpath('//div[@class="qphox"]//div[@class="sckifbox"]//div[@class="scklox"]//div[@class="cnt"]//text()')[2].replace(' ', '')[1:]

            print(file[-6:])
            print("\n")
            self._csvfile.write(file[-6:])  #add ID 

            self._csvfile.write(',')
            self._csvfile.write(nameTmp)    #add Name

            count = 0
            for ele in dom.body.xpath('//div[@class="section"]'):
                if ele[0].attrib['id'] == "sdltgd":
                    eleTmp = ele[1]
                    for eleTmp1 in eleTmp.xpath('//div[@class="tab"]//span//text()'):
                        count += 1
                        self._csvfile.write(',')
                        self._csvfile.write(eleTmp1)    #add Date
                        pass
                    if count < 5:
                        for i in range(0, 5 - count):
                            self._csvfile.write(',')

                    for eleTmp1 in eleTmp.xpath('.//div[@class="content first"][@id="TTCS_Table_Div"]//table'):
                        self._csvfile.write(',')
                        self._csvfile.write("@@")    #add Date
                        for eleTmp2 in eleTmp1.xpath('.//td[@class="tips-dataL"]//text()'):
                            eleTmp2 = eleTmp2.replace(',', '')
                            self._csvfile.write(',')
                            self._csvfile.write(eleTmp2)    #add Data
                else:
                    continue           

            self._csvfile.write('\n')
            fileobj.close()
        except:
            pass

    def generateLog(self):
        self.getFileSet()
        i = 0
        for ele in self._fileSet:
            i += 1
            print(i)   
            print ele         
            self.generateALine(ele)
        self._csvfile.close()
        pass


LogInstance = LogManager();
LogInstance.generateLog()