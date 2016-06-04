from DataCollecter import *
import thread
from threading import Thread
DataInstance = DataCollecter();

class MyThread(Thread):
	"""docstring for MyThread"""
	def __init__(self, name, IDList):
		super(MyThread, self).__init__()
		self.name = name
		self.IDList = IDList

	def run(self):
		DataInstance.UpdateStocksHtmls(self.name, self.IDList)

#DataInstance.UpdateStocks("sz", 9000001,9000999)
#DataInstance.UpdateStocks("sz", 9002167,9002740)
#DataInstance.UpdateStocks("sz", 9300001,9300500)


#DataInstance.UpdateStocks("sh", 9601801,9602000)
#DataInstance.UpdateStocks("sh", 9600000,9604000)


#DataInstance.UpdateStockname("stname.txt")
#DataInstance.NewTab("stname.txt")
#DataInstance.UpdateStocksHtmls("sz", 9000001,9000999)

namefile = open('stname.txt', 'r')

IDList = []
countID = 0
for line in namefile.readlines():
    countID += 1
    if countID == 1 : continue
    txt = line.decode('utf8')
    IDList.append('9' + txt.split('\t')[1].replace('\'', ''))
    pass

IDListsz1 = []
IDListsz2 = []
IDListsz3 = []
IDListsh1 = []
IDListsh2 = []

for i in range(0, countID - 1):
    IDIt = IDList[i]
    if int(IDIt) <= 9000999: IDListsz1.append(IDIt)
    elif int(IDIt) >= 9002000 and int(IDIt) <= 9003000 : IDListsz2.append(IDIt)
    elif int(IDIt) >= 9300001 and int(IDIt) <= 9300420 : IDListsz3.append(IDIt)
    elif int(IDIt) >= 9600000 and int(IDIt) <= 9602000 : IDListsh1.append(IDIt)
    elif int(IDIt) >= 9603000 and int(IDIt) <= 9604000 : IDListsh2.append(IDIt)
    else : pass

TH1 = MyThread("sz", IDListsz1)
TH2 = MyThread("sz", IDListsz2)
TH3 = MyThread("sz", IDListsz3)
TH4 = MyThread("sh", IDListsh1)
TH5 = MyThread("sh", IDListsh2)

TH1.start()
TH2.start()
TH3.start()
TH4.start()
TH5.start()
#thread.start_new_thread(DataInstance.UpdateStocksHtmls, ("sz", 9000001,9000999))
'''thread.start_new_thread(DataInstance.UpdateStocksHtmls, ("sz", 9002001,9002780))
thread.start_new_thread(DataInstance.UpdateStocksHtmls, ("sz", 9300001,9300420))
thread.start_new_thread(DataInstance.UpdateStocksHtmls, ("sh", 9600000,9602000))
thread.start_new_thread(DataInstance.UpdateStocksHtmls, ("sh", 9603000,9604000))
'''