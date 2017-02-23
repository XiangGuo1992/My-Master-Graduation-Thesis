import os
from pandas import read_table 
from pandas import read_csv 
os.chdir('F:\\GuoXiang\\硕士毕业论文\\DATA\\physiological\\1_rawdata')              #变更工作目录
listfile = os.listdir()                                             #列出所有文件
print (listfile)
timedelay = read_csv('F:/GuoXiang/硕士毕业论文/DATA/physiological/physio_starttime.csv',encoding='gbk')


for x in listfile:
	
	PhysioData =  read_table(x, header = None)
	data = PhysioData.ix[:,[0,4]]
	data.columns = ['time','HR']
	SubjectNum = int(x.split(sep = '.')[0])           #获得被试编号
	data['time'] = (data['time'] - float(timedelay['Start'][timedelay['Subject']==SubjectNum]))*60
	data = data[data['time']>0]


	filename = 'F:\\GuoXiang\\硕士毕业论文\\DATA\\physiological\\2_csv\\' + x.split(sep = '.')[0] + '.csv'     #保存的文件名定义 
	data.to_csv(filename,index = False)                    #输出.csv文件     
	

 

