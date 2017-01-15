import os
import numpy as np
import pandas as pd
from pandas import read_table 
from pandas import read_csv 
os.chdir('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyeprolog\\1_rawdata')              #变更工作目录
listfile = os.listdir()                                             #列出所有文件
print (listfile)

driving_start = read_csv('F:/GuoXiang/硕士毕业论文/DATA/eye/driving_start.csv',encoding='gbk')

for x in listfile:                                                  #批量处理                                      
	data = read_table(x)                                            #读取文件
	dataNum = int(x.split(sep = '.')[0])            #分离文件名中的数字
	start_index = list(driving_start['subject']).index(dataNum)    #得到对应文件名的索引号

	data['time'] = (data['UserTimeStamp']- data.ix[0,'UserTimeStamp'])/10000000  - driving_start['start_time'][start_index]           #增加一列修正后的时间
	eyedata = data[['time','Blink','Fixation','Saccade']][data['time']>0]         #筛选出质量大于0.5的时间，heading,pitch数据
	filename = 'F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyeprolog\\2_procsv\\' + x.split(sep = '.')[0] + '.csv'     #保存的文件名定义 
	eyedata.to_csv(filename,index = False)                    #输出.csv文件
     
     
 

