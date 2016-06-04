import urllib2
import string
from sgmllib import SGMLParser
class EastmoneyContent(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_table0 = 0
        self.text = []
        self.is_th = 0
        self.is_td = 0
        self.is_tr = 0
        self.BeginCountRow = 0
        self.CountOfRow = 0
        self.CountOfColumn = 0
        self.listmatrix = []

    def start_table(self, attrs):
        if len(attrs) == 0 : pass
        else:
            for (variable1, value1) in attrs:
               if (value1 == "Table0"):
                   self.is_table0 = 1

    def end_table(self):        
        self.is_table0 = 0

    def start_tr(self, attrs):
        if (self.is_table0 == 1) :
            self.CountOfColumn += 1

    def end_tr(self):
        self.BeginCountRow = 0
        pass   

    def start_th(self, attrs):
        if (self.is_table0 == 1) :            
            for (attrname, attrcontent) in attrs:
                if attrcontent == "tips-colnameL":
                    self.BeginCountRow = 1
                if attrcontent == "tips-dataL":
                    self.is_th = 1
                    if self.BeginCountRow == 1:
                        self.CountOfRow += 1
                

    def end_th(self):
        self.is_th = 0

    def start_td(self, attrs):
        if self.is_table0 == 1 :
            for(attrname, attrcontent) in attrs:
                if attrcontent == "tips-dataL":
                    self.is_td = 1
    
    def end_td(self):
        self.is_td = 0

    def handle_data(self, text):
        if (self.is_th == 1 or self.is_td == 1):
            if text[-3:] == '\xe4\xb8\x87':
                numtext = text[0:(len(text)-3)]
                number = string.atof(numtext) * 10000;
                numbertextnew = str(number)
                self.text.append(numbertextnew)
            else:
                self.text.append(text)

    def handle_listmatrix(self, code, type):
        listtmp = []        
        for index in range(0,self.CountOfRow):
            listtmp1 = []
            listtmp = [code, type] + self.text[index : len(self.text) : (self.CountOfRow)]
            for item in listtmp:
                listtmp1.append(item)
                pass
            self.listmatrix.append(tuple(listtmp1)) #executemany method of sqlite needs tuple
            pass
 