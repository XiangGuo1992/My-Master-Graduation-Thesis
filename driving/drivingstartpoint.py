import os
import numpy as np
import pandas as pd
from pandas import read_csv 
os.chdir('F:\\GuoXiang\\硕士毕业论文\\DATA\\data\\1_rawdata')              #变更工作目录
listfile = os.listdir()                                             #列出所有文件
print (listfile)

a = pd.DataFrame(np.zeros((len(listfile),2)))  
for x in listfile:    #批量处理
	drivingdata = read_csv(x)  #读取文件	
	A = drivingdata[(drivingdata['Type']=='uv') & (drivingdata["Time"] >0)]['Time']
	A.index = range(len(A))
	a.ix[listfile.index(x),0] = x
	a.ix[listfile.index(x),1] = A[0]
a.to_csv('driving_start.csv',index = False)                    #输出.csv文件		       
