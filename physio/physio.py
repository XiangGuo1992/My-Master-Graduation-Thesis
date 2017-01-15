import os
from pandas import read_table 
os.chdir('F:\\GuoXiang\\硕士毕业论文\\DATA\\physiological\\1_rawdata')              #变更工作目录
listfile = os.listdir()                                             #列出所有文件
print (listfile)



for x in listfile:
	
	ProData =  read_table(x)
	


	filename = 'F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyeprolog\\2_fix&sac\\' + x.split(sep = '.')[0] + '.csv'     #保存的文件名定义 
	ProData.to_csv(filename,index = False)                    #输出.csv文件     
	

 

