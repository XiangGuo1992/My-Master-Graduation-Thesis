import os
import numpy as np
import pandas as pd
from pandas import read_csv 
os.chdir('F:\\硕士毕业论文\\DATA\\physiological\\2_csv')              #变更工作目录
listfile = os.listdir()                                             #列出所有文件
print (listfile)
timepoint = read_csv('F:/硕士毕业论文/DATA/physiological/时间节点汇总表.csv',encoding='gbk')



for x in listfile:    #批量处理
	data = read_csv(x)  #读取文件
	
	dataNum = int(x.split(sep = '.')[0])            #分离文件名中的数字
	start_index = list(timepoint['subject']).index(dataNum)    #得到对应文件名的索引号
	A=pd.DataFrame(np.zeros((6,5)))
	A.ix[:,0]=dataNum	

	for i in range(1,7):
		Time = timepoint.ix[start_index,i]
		to_before = data[(data['time'] > (Time-30)) & (data['time'] < Time)]
		to_after = data[(data['time'] > Time) & (data['time'] < (Time+30))]

		A.ix[i-1,1]= np.mean(to_before['HR'])    #第二列为接管前心率平均值
		A.ix[i-1,2]= np.mean(to_after['HR'])    #第三列为接管后心率平均值
		A.ix[i-1,3]= np.std(to_before['HR'],ddof =1)    #第四列为接管前心率标准差
		A.ix[i-1,4]= np.std(to_after['HR'],ddof =1)    #第五列为接管后心率标准差

	filenames = 'F:\\硕士毕业论文\\DATA\\physiological\\3_HR\\' + x 
	A.columns = ['subject','HR_mean_before','HR_mean_after','HR_sd_before','HR_sd_after']

	A.to_csv(filenames,index = False)




