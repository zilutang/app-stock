import string

class URLBuilder():
    def __init__(self):
        self._urlToGet = ""

    def GetURL(self, component):
        self._urlToGet = 'http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code=' + component
        #self._urlToGet = 'http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code=' + component
        print "catching " + component + "...  "
        return self._urlToGet
