import os
from pandas import read_table 
import math
os.chdir('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyerecorderdata\\1_rawdata')              #变更工作目录
listfile = os.listdir()                                             #列出所有文件
print (listfile)

for x in listfile:                                                  #批量处理                                      
	data = read_table(x)                                            #读取文件
	data['time'] = (data['UserTimeStamp']- data.ix[0,'UserTimeStamp'])/10000000           #增加一列修正后的时间
	eyedata = data[['time','GazeHeading','GazePitch','GazeOrigin.x','GazeOrigin.y','GazeOrigin.z','GazeDirection.x','GazeDirection.y','GazeDirection.z']][data['GazeDirectionQ']>0.5]         #筛选出质量大于0.5的时间，heading,pitch数据
	#单位转化 
	eyedata['GazeHeading'][eyedata['GazeHeading'] > 0] = 180-eyedata['GazeHeading'][eyedata['GazeHeading'] > 0]*180/math.pi
	eyedata['GazeHeading'][eyedata['GazeHeading'] < 0] = -eyedata['GazeHeading'][eyedata['GazeHeading'] < 0]*180/math.pi -180
	eyedata['GazePitch'] = eyedata['GazePitch']*180/math.pi
	eyedata['GazeDirection.x'] = eyedata['GazeDirection.x']*180/math.pi
	eyedata['GazeDirection.y'] = eyedata['GazeDirection.y']*180/math.pi
	eyedata['GazeDirection.z'] = eyedata['GazeDirection.z']*180/math.pi
	filename = 'F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyerecorderdata\\2_filterdata\\' + x.split(sep = '.')[0] + '.csv'     #保存的文件名定义 
	eyedata.to_csv(filename,index = False)                    #输出.csv文件
     
     
 

