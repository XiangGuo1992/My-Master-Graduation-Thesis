import os
from pandas import read_table 
os.chdir('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyeprolog\\1_rawdata')              #变更工作目录
listfile = os.listdir()                                             #列出所有文件
print (listfile)

#recorder 目录
RecorderDir = 'F:/GuoXiang/硕士毕业论文/DATA/eye/eyerecorderdata/1_rawdata/'

for x in listfile:
	RecorderName = RecorderDir + x   
	ProData =  read_table(x)
	RecorderData = read_table(RecorderName)
	RecorderData['time'] = (RecorderData['UserTimeStamp']- RecorderData.ix[0,'UserTimeStamp'])/10000000 

	head_index = list(RecorderData['HeadPosition.x']).index(ProData['HeadPosition.x'][0])
	RecorderDataSec = RecorderData.ix[head_index:(head_index+len(ProData)-1), ['time','GazeHeading','GazePitch','GazeDirectionQ']]

	RecorderDataSec.index = range(len(RecorderDataSec))
	RecorderDataSec['Blink'] = ProData['Blink']
	RecorderDataSec['Fixation'] = ProData['Fixation']
	RecorderDataSec['Saccade'] = ProData['Saccade']

	filename = 'F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyeprolog\\2_fix&sac\\' + x.split(sep = '.')[0] + '.csv'     #保存的文件名定义 
	RecorderDataSec.to_csv(filename,index = False)                    #输出.csv文件     
	

 

