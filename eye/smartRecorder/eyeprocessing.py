# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 10:22:47 2016

@author: sqc
"""

import os
import numpy as np
import pandas as pd
from pandas import read_csv 
os.chdir('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyerecorderdata\\2_filterdata')              #变更工作目录
listfile = os.listdir()                                             #列出所有文件
print (listfile)

#驾驶时间节点
timepoint = read_csv('F:/GuoXiang/硕士毕业论文/DATA/eye/timepoint.csv',encoding='gbk')
#眼动数据延迟
timedelay = read_csv('F:/GuoXiang/硕士毕业论文/DATA/eye/timedelay.csv',encoding='gbk')


#定义浮点型range函数
def floatrange(start,stop,steps):
	return [start+float(i)*(stop-start)/(float(steps)-1) for i in range(steps)]

#查找道路中心函数
def findRC(x):
    bins = floatrange(min(x),max(x),int(x.max()-x.min()))
    n=np.zeros((len(bins),2))
    x = np.array(x)
    for i in range(len(bins)-1):
        n[i,0] = (bins[i] + bins[i+1])/2
        a = x[(x>bins[i])& (x<bins[i+1])]
        n[i,1] = len(a)
    return n[:,0][n[:,1] == n[:,1].max()].mean()
    

#计算距离及百分比
def calDTC(heading,pithch,x,y):
	j=0
	heading.index = range(len(heading))
	pithch.index = range(len(pithch))
	n = len(heading)
	for i in range(n):
		if (((heading[i]-x)**2+(pithch[i]-y)**2)**0.5 < 16):
			j += 1
	return j/n



#批量处理  
for x in listfile:
	data = read_csv(x)
	#时间修正
	SubjectNum = int(x.split(sep = '.')[0])           #获得被试编号
	data['time'] = data['time'] - float(timedelay['StartPoint'][timedelay['Subject']==SubjectNum])
	data = data[data['time']>= 0]
	data.index = range(len(data))

	HeadingCenter = findRC(data['GazeHeading'])
	PitchCenter = findRC(data['GazePitch'])
	

	 #变量A存储PRC值
	A= pd.DataFrame(np.empty((6,17)))   

	#第一段5km处非紧急接管
	f1TimePoint = float(timepoint['5km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(f1TimePoint-60)]
	f1before = temp1[temp1['time']< f1TimePoint]	
	temp2 = data[data['time']> f1TimePoint]
	f1after = temp2[temp2['time'] < (f1TimePoint + 30)]
	f1 = temp1[temp1['time'] < (f1TimePoint + 30)]

	A.ix[0,0] = x             #第一列为文件名
	A.ix[0,1] = 0             #第二列为次任务类型
	A.ix[0,2] = 0             #第三列为紧急类型
	A.ix[0,3] = calDTC(f1before['GazeHeading'],f1before['GazePitch'],HeadingCenter,PitchCenter)   #第四列为接管前PRC
	A.ix[0,4] = calDTC(f1after['GazeHeading'],f1after['GazePitch'],HeadingCenter,PitchCenter)     #第五列为接管后PRC
	A.ix[0,5] = findRC(f1['GazeHeading'])                      #第六列为事件的水平注视中心
	A.ix[0,6] = findRC(f1['GazePitch'])                        #第七列为事件的垂直注视中心
	A.ix[0,7] = findRC(f1before['GazeHeading'])                #第8列为接管前水平注视中心
	A.ix[0,8] = findRC(f1before['GazePitch'])                  #第9列为接管前垂直注视中心
	A.ix[0,9] = findRC(f1after['GazeHeading'])                 #第10列为接管后水平注视中心
	A.ix[0,10] = findRC(f1after['GazePitch'])                  #第11列为接管后垂直注视中心
	A.ix[0,11] = np.std(f1['GazeHeading'])                      #第12列为事件的水平注视标准差
	A.ix[0,12] = np.std(f1['GazePitch'])                        #第13列为事件的垂直注视标准差
	A.ix[0,13] = np.std(f1before['GazeHeading'])                #第14列为接管前水平注视标准差
	A.ix[0,14] = np.std(f1before['GazePitch'])                  #第15列为接管前垂直注视标准差
	A.ix[0,15] = np.std(f1after['GazeHeading'])                 #第16列为接管后水平注视标准差
	A.ix[0,16] = np.std(f1after['GazePitch'])                  #第17列为接管后垂直注视标准差

	#第二段10km紧急接管
	b1TimePoint = float(timepoint['10km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(b1TimePoint-60)]
	b1before = temp1[temp1['time']< b1TimePoint]	
	temp2 = data[data['time']> b1TimePoint]
	b1after = temp2[temp2['time'] < (b1TimePoint + 30)]
	b1 = temp1[temp1['time'] < (b1TimePoint + 30)]

	A.ix[1,0] = x
	A.ix[1,1] = 0
	A.ix[1,2] = 1
	A.ix[1,3] = calDTC(b1before['GazeHeading'],b1before['GazePitch'],findRC(b1before['GazeHeading']),findRC(b1before['GazePitch']))
	A.ix[1,4] = calDTC(b1after['GazeHeading'],b1after['GazePitch'],findRC(b1after['GazeHeading']),findRC(b1after['GazePitch']))
	A.ix[1,5] = findRC(b1['GazeHeading'])                      #第六列为事件的水平注视中心
	A.ix[1,6] = findRC(b1['GazePitch'])                        #第七列为事件的垂直注视中心
	A.ix[1,7] = findRC(b1before['GazeHeading'])                #第8列为接管前水平注视中心
	A.ix[1,8] = findRC(b1before['GazePitch'])                  #第9列为接管前垂直注视中心
	A.ix[1,9] = findRC(b1after['GazeHeading'])                 #第10列为接管后水平注视中心
	A.ix[1,10] = findRC(b1after['GazePitch'])                  #第11列为接管后垂直注视中心
	A.ix[1,11] = np.std(b1['GazeHeading'])                      #第12列为事件的水平注视标准差
	A.ix[1,12] = np.std(b1['GazePitch'])                        #第13列为事件的垂直注视标准差
	A.ix[1,13] = np.std(b1before['GazeHeading'])                #第14列为接管前水平注视标准差
	A.ix[1,14] = np.std(b1before['GazePitch'])                  #第15列为接管前垂直注视标准差
	A.ix[1,15] = np.std(b1after['GazeHeading'])                 #第16列为接管后水平注视标准差
	A.ix[1,16] = np.std(b1after['GazePitch'])                  #第17列为接管后垂直注视标准差


	#第3段17km非紧急接管
	f2TimePoint = float(timepoint['17km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(f2TimePoint-60)]
	f2before = temp1[temp1['time']< f2TimePoint]	
	temp2 = data[data['time']> f2TimePoint]
	f2after = temp2[temp2['time'] < (f2TimePoint + 30)]
	f2 = temp1[temp1['time'] < (f2TimePoint + 30)]

	A.ix[2,0] = x
	A.ix[2,1] = 1
	A.ix[2,2] = 0
	A.ix[2,3] = calDTC(f2before['GazeHeading'],f2before['GazePitch'],findRC(f2before['GazeHeading']),findRC(f2before['GazePitch']))
	A.ix[2,4] = calDTC(f2after['GazeHeading'],f2after['GazePitch'],findRC(f2after['GazeHeading']),findRC(f2after['GazePitch']))
	A.ix[2,5] = findRC(f2['GazeHeading'])                      #第六列为事件的水平注视中心
	A.ix[2,6] = findRC(f2['GazePitch'])                        #第七列为事件的垂直注视中心
	A.ix[2,7] = findRC(f2before['GazeHeading'])                #第8列为接管前水平注视中心
	A.ix[2,8] = findRC(f2before['GazePitch'])                  #第9列为接管前垂直注视中心
	A.ix[2,9] = findRC(f2after['GazeHeading'])                 #第10列为接管后水平注视中心
	A.ix[2,10] = findRC(f2after['GazePitch'])                  #第11列为接管后垂直注视中心
	A.ix[2,11] = np.std(f2['GazeHeading'])                      #第12列为事件的水平注视标准差
	A.ix[2,12] = np.std(f2['GazePitch'])                        #第13列为事件的垂直注视标准差
	A.ix[2,13] = np.std(f2before['GazeHeading'])                #第14列为接管前水平注视标准差
	A.ix[2,14] = np.std(f2before['GazePitch'])                  #第15列为接管前垂直注视标准差
	A.ix[2,15] = np.std(f2after['GazeHeading'])                 #第16列为接管后水平注视标准差
	A.ix[2,16] = np.std(f2after['GazePitch'])                  #第17列为接管后垂直注视标准差

	#第4段22km紧急接管
	f2TimePoint2 = float(timepoint['22km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(f2TimePoint2-60)]
	f2before2 = temp1[temp1['time']< f2TimePoint2]	
	temp2 = data[data['time']> f2TimePoint2]
	f2after2 = temp2[temp2['time'] < (f2TimePoint2 + 30)]
	f22 = temp1[temp1['time'] < (f2TimePoint2 + 30)]

	A.ix[3,0] = x
	A.ix[3,1] = 1
	A.ix[3,2] = 1
	A.ix[3,3] = calDTC(f2before2['GazeHeading'],f2before2['GazePitch'],findRC(f2before2['GazeHeading']),findRC(f2before2['GazePitch']))
	A.ix[3,4] = calDTC(f2after2['GazeHeading'],f2after2['GazePitch'],findRC(f2after2['GazeHeading']),findRC(f2after2['GazePitch']))
	A.ix[3,5] = findRC(f22['GazeHeading'])                      #第六列为事件的水平注视中心
	A.ix[3,6] = findRC(f22['GazePitch'])                        #第七列为事件的垂直注视中心
	A.ix[3,7] = findRC(f2before2['GazeHeading'])                #第8列为接管前水平注视中心
	A.ix[3,8] = findRC(f2before2['GazePitch'])                  #第9列为接管前垂直注视中心
	A.ix[3,9] = findRC(f2after2['GazeHeading'])                 #第10列为接管后水平注视中心
	A.ix[3,10] = findRC(f2after2['GazePitch'])                  #第11列为接管后垂直注视中心
	A.ix[3,11] = np.std(f22['GazeHeading'])                      #第12列为事件的水平注视标准差
	A.ix[3,12] = np.std(f22['GazePitch'])                        #第13列为事件的垂直注视标准差
	A.ix[3,13] = np.std(f2before2['GazeHeading'])                #第14列为接管前水平注视标准差
	A.ix[3,14] = np.std(f2before2['GazePitch'])                  #第15列为接管前垂直注视标准差
	A.ix[3,15] = np.std(f2after2['GazeHeading'])                 #第16列为接管后水平注视标准差
	A.ix[3,16] = np.std(f2after2['GazePitch'])                  #第17列为接管后垂直注视标准差

	#第5段29km非紧急接管
	b2TimePoint = float(timepoint['29km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(b2TimePoint-60)]
	b2before = temp1[temp1['time']< b2TimePoint]	
	temp2 = data[data['time']> b2TimePoint]
	b2after = temp2[temp2['time'] < (b2TimePoint + 30)]
	b2 = temp1[temp1['time'] < (b2TimePoint + 30)]

	A.ix[4,0] = x
	A.ix[4,1] = 2
	A.ix[4,2] = 0
	A.ix[4,3] = calDTC(b2before['GazeHeading'],b2before['GazePitch'],findRC(b2before['GazeHeading']),findRC(b2before['GazePitch']))
	A.ix[4,4] = calDTC(b2after['GazeHeading'],b2after['GazePitch'],findRC(b2after['GazeHeading']),findRC(b2after['GazePitch']))
	A.ix[4,5] = findRC(b2['GazeHeading'])                      #第六列为事件的水平注视中心
	A.ix[4,6] = findRC(b2['GazePitch'])                        #第七列为事件的垂直注视中心
	A.ix[4,7] = findRC(b2before['GazeHeading'])                #第8列为接管前水平注视中心
	A.ix[4,8] = findRC(b2before['GazePitch'])                  #第9列为接管前垂直注视中心
	A.ix[4,9] = findRC(b2after['GazeHeading'])                 #第10列为接管后水平注视中心
	A.ix[4,10] = findRC(b2after['GazePitch'])                  #第11列为接管后垂直注视中心
	A.ix[4,11] = np.std(b2['GazeHeading'])                      #第12列为事件的水平注视标准差
	A.ix[4,12] = np.std(b2['GazePitch'])                        #第13列为事件的垂直注视标准差
	A.ix[4,13] = np.std(b2before['GazeHeading'])                #第14列为接管前水平注视标准差
	A.ix[4,14] = np.std(b2before['GazePitch'])                  #第15列为接管前垂直注视标准差
	A.ix[4,15] = np.std(b2after['GazeHeading'])                 #第16列为接管后水平注视标准差
	A.ix[4,16] = np.std(b2after['GazePitch'])                  #第17列为接管后垂直注视标准差

	#第6段34km紧急接管
	f3TimePoint = float(timepoint['34km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(f3TimePoint-60)]
	f3before = temp1[temp1['time']< f3TimePoint]	
	temp2 = data[data['time']> f3TimePoint]
	f3after = temp2[temp2['time'] < (f3TimePoint + 30)]
	f3 = temp1[temp1['time'] < (f3TimePoint + 30)]

	A.ix[5,0] = x
	A.ix[5,1] = 2
	A.ix[5,2] = 1
	A.ix[5,3] = calDTC(f3before['GazeHeading'],f3before['GazePitch'],findRC(f3before['GazeHeading']),findRC(f3before['GazePitch']))
	A.ix[5,4] = calDTC(f3after['GazeHeading'],f3after['GazePitch'],findRC(f3after['GazeHeading']),findRC(f3after['GazePitch']))
	A.ix[5,5] = findRC(f3['GazeHeading'])                      #第六列为事件的水平注视中心
	A.ix[5,6] = findRC(f3['GazePitch'])                        #第七列为事件的垂直注视中心
	A.ix[5,7] = findRC(f3before['GazeHeading'])                #第8列为接管前水平注视中心
	A.ix[5,8] = findRC(f3before['GazePitch'])                  #第9列为接管前垂直注视中心
	A.ix[5,9] = findRC(f3after['GazeHeading'])                 #第10列为接管后水平注视中心
	A.ix[5,10] = findRC(f3after['GazePitch'])                  #第11列为接管后垂直注视中心
	A.ix[5,11] = np.std(f3['GazeHeading'])                      #第12列为事件的水平注视标准差
	A.ix[5,12] = np.std(f3['GazePitch'])                        #第13列为事件的垂直注视标准差
	A.ix[5,13] = np.std(f3before['GazeHeading'])                #第14列为接管前水平注视标准差
	A.ix[5,14] = np.std(f3before['GazePitch'])                  #第15列为接管前垂直注视标准差
	A.ix[5,15] = np.std(f3after['GazeHeading'])                 #第16列为接管后水平注视标准差
	A.ix[5,16] = np.std(f3after['GazePitch'])                  #第17列为接管后垂直注视标准差

	A.columns = ['subject','secondarytask','emergency','before_PRC','after_PRC','EventHeadingCenter','EventPithchCenter','beforeHeadingCenter','beforePitchCenter',
	'afterHeadingCenter','afterPitchCenter','EventHeadingSD','EventPithchSD','beforeHeadingSD','beforePitchSD','afterHeadingSD','afterPitchSD']
	A.to_csv('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyerecorderdata\\3_PRC\\' + 'PRC_' + x,index = False,)
	

'''
#单个 
x = '411.csv'
data = read_csv(x)
#时间修正
SubjectNum = int(x.split(sep = '.')[0])           #获得被试编号
data['time'] = data['time'] - float(timedelay['StartPoint'][timedelay['Subject']==SubjectNum])
data = data[data['time']>= 0]
data.index = range(len(data))


 #变量A存储PRC值
A= pd.DataFrame(np.empty((6,17)))   
#第一段5km处非紧急接管
f1TimePoint = float(timepoint['5km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(f1TimePoint-60)]
f1before = temp1[temp1['time']< f1TimePoint]	
temp2 = data[data['time']> f1TimePoint]
f1after = temp2[temp2['time'] < (f1TimePoint + 30)]
f1 = temp1[temp1['time'] < (f1TimePoint + 30)]

A.ix[0,0] = x             #第一列为文件名
A.ix[0,1] = 0             #第二列为次任务类型
A.ix[0,2] = 0             #第三列为紧急类型
A.ix[0,3] = calDTC(f1before['GazeHeading'],f1before['GazePitch'],findRC(f1before['GazeHeading']),findRC(f1before['GazePitch']))   #第四列为接管前PRC
A.ix[0,4] = calDTC(f1after['GazeHeading'],f1after['GazePitch'],findRC(f1after['GazeHeading']),findRC(f1after['GazePitch']))     #第五列为接管后PRC
A.ix[0,5] = findRC(f1['GazeHeading'])                      #第六列为事件的水平注视中心
A.ix[0,6] = findRC(f1['GazePitch'])                        #第七列为事件的垂直注视中心
A.ix[0,7] = findRC(f1before['GazeHeading'])                #第8列为接管前水平注视中心
A.ix[0,8] = findRC(f1before['GazePitch'])                  #第9列为接管前垂直注视中心
A.ix[0,9] = findRC(f1after['GazeHeading'])                 #第10列为接管后水平注视中心
A.ix[0,10] = findRC(f1after['GazePitch'])                  #第11列为接管后垂直注视中心
A.ix[0,11] = np.std(f1['GazeHeading'])                      #第12列为事件的水平注视标准差
A.ix[0,12] = np.std(f1['GazePitch'])                        #第13列为事件的垂直注视标准差
A.ix[0,13] = np.std(f1before['GazeHeading'])                #第14列为接管前水平注视标准差
A.ix[0,14] = np.std(f1before['GazePitch'])                  #第15列为接管前垂直注视标准差
A.ix[0,15] = np.std(f1after['GazeHeading'])                 #第16列为接管后水平注视标准差
A.ix[0,16] = np.std(f1after['GazePitch'])                  #第17列为接管后垂直注视标准差

#第二段10km紧急接管
b1TimePoint = float(timepoint['10km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(b1TimePoint-60)]
b1before = temp1[temp1['time']< b1TimePoint]	
temp2 = data[data['time']> b1TimePoint]
b1after = temp2[temp2['time'] < (b1TimePoint + 30)]
b1 = temp1[temp1['time'] < (b1TimePoint + 30)]

A.ix[1,0] = x
A.ix[1,1] = 0
A.ix[1,2] = 1
A.ix[1,3] = calDTC(b1before['GazeHeading'],b1before['GazePitch'],findRC(b1before['GazeHeading']),findRC(b1before['GazePitch']))
A.ix[1,4] = calDTC(b1after['GazeHeading'],b1after['GazePitch'],findRC(b1after['GazeHeading']),findRC(b1after['GazePitch']))
A.ix[1,5] = findRC(b1['GazeHeading'])                      #第六列为事件的水平注视中心
A.ix[1,6] = findRC(b1['GazePitch'])                        #第七列为事件的垂直注视中心
A.ix[1,7] = findRC(b1before['GazeHeading'])                #第8列为接管前水平注视中心
A.ix[1,8] = findRC(b1before['GazePitch'])                  #第9列为接管前垂直注视中心
A.ix[1,9] = findRC(b1after['GazeHeading'])                 #第10列为接管后水平注视中心
A.ix[1,10] = findRC(b1after['GazePitch'])                  #第11列为接管后垂直注视中心
A.ix[1,11] = np.std(b1['GazeHeading'])                      #第12列为事件的水平注视标准差
A.ix[1,12] = np.std(b1['GazePitch'])                        #第13列为事件的垂直注视标准差
A.ix[1,13] = np.std(b1before['GazeHeading'])                #第14列为接管前水平注视标准差
A.ix[1,14] = np.std(b1before['GazePitch'])                  #第15列为接管前垂直注视标准差
A.ix[1,15] = np.std(b1after['GazeHeading'])                 #第16列为接管后水平注视标准差
A.ix[1,16] = np.std(b1after['GazePitch'])                  #第17列为接管后垂直注视标准差


#第3段17km非紧急接管
f2TimePoint = float(timepoint['17km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(f2TimePoint-60)]
f2before = temp1[temp1['time']< f2TimePoint]	
temp2 = data[data['time']> f2TimePoint]
f2after = temp2[temp2['time'] < (f2TimePoint + 30)]
f2 = temp1[temp1['time'] < (f2TimePoint + 30)]

A.ix[2,0] = x
A.ix[2,1] = 1
A.ix[2,2] = 0
A.ix[2,3] = calDTC(f2before['GazeHeading'],f2before['GazePitch'],findRC(f2before['GazeHeading']),findRC(f2before['GazePitch']))
A.ix[2,4] = calDTC(f2after['GazeHeading'],f2after['GazePitch'],findRC(f2after['GazeHeading']),findRC(f2after['GazePitch']))
A.ix[2,5] = findRC(f2['GazeHeading'])                      #第六列为事件的水平注视中心
A.ix[2,6] = findRC(f2['GazePitch'])                        #第七列为事件的垂直注视中心
A.ix[2,7] = findRC(f2before['GazeHeading'])                #第8列为接管前水平注视中心
A.ix[2,8] = findRC(f2before['GazePitch'])                  #第9列为接管前垂直注视中心
A.ix[2,9] = findRC(f2after['GazeHeading'])                 #第10列为接管后水平注视中心
A.ix[2,10] = findRC(f2after['GazePitch'])                  #第11列为接管后垂直注视中心
A.ix[2,11] = np.std(f2['GazeHeading'])                      #第12列为事件的水平注视标准差
A.ix[2,12] = np.std(f2['GazePitch'])                        #第13列为事件的垂直注视标准差
A.ix[2,13] = np.std(f2before['GazeHeading'])                #第14列为接管前水平注视标准差
A.ix[2,14] = np.std(f2before['GazePitch'])                  #第15列为接管前垂直注视标准差
A.ix[2,15] = np.std(f2after['GazeHeading'])                 #第16列为接管后水平注视标准差
A.ix[2,16] = np.std(f2after['GazePitch'])                  #第17列为接管后垂直注视标准差

#第4段22km紧急接管
f2TimePoint2 = float(timepoint['22km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(f2TimePoint2-60)]
f2before2 = temp1[temp1['time']< f2TimePoint2]	
temp2 = data[data['time']> f2TimePoint2]
f2after2 = temp2[temp2['time'] < (f2TimePoint2 + 30)]
f22 = temp1[temp1['time'] < (f2TimePoint2 + 30)]

A.ix[3,0] = x
A.ix[3,1] = 1
A.ix[3,2] = 1
A.ix[3,3] = calDTC(f2before2['GazeHeading'],f2before2['GazePitch'],findRC(f2before2['GazeHeading']),findRC(f2before2['GazePitch']))
A.ix[3,4] = calDTC(f2after2['GazeHeading'],f2after2['GazePitch'],findRC(f2after2['GazeHeading']),findRC(f2after2['GazePitch']))
A.ix[3,5] = findRC(f22['GazeHeading'])                      #第六列为事件的水平注视中心
A.ix[3,6] = findRC(f22['GazePitch'])                        #第七列为事件的垂直注视中心
A.ix[3,7] = findRC(f2before2['GazeHeading'])                #第8列为接管前水平注视中心
A.ix[3,8] = findRC(f2before2['GazePitch'])                  #第9列为接管前垂直注视中心
A.ix[3,9] = findRC(f2after2['GazeHeading'])                 #第10列为接管后水平注视中心
A.ix[3,10] = findRC(f2after2['GazePitch'])                  #第11列为接管后垂直注视中心
A.ix[3,11] = np.std(f22['GazeHeading'])                      #第12列为事件的水平注视标准差
A.ix[3,12] = np.std(f22['GazePitch'])                        #第13列为事件的垂直注视标准差
A.ix[3,13] = np.std(f2before2['GazeHeading'])                #第14列为接管前水平注视标准差
A.ix[3,14] = np.std(f2before2['GazePitch'])                  #第15列为接管前垂直注视标准差
A.ix[3,15] = np.std(f2after2['GazeHeading'])                 #第16列为接管后水平注视标准差
A.ix[3,16] = np.std(f2after2['GazePitch'])                  #第17列为接管后垂直注视标准差

#第5段29km非紧急接管
b2TimePoint = float(timepoint['29km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(b2TimePoint-60)]
b2before = temp1[temp1['time']< b2TimePoint]	
temp2 = data[data['time']> b2TimePoint]
b2after = temp2[temp2['time'] < (b2TimePoint + 30)]
b2 = temp1[temp1['time'] < (b2TimePoint + 30)]

A.ix[4,0] = x
A.ix[4,1] = 2
A.ix[4,2] = 0
A.ix[4,3] = calDTC(b2before['GazeHeading'],b2before['GazePitch'],findRC(b2before['GazeHeading']),findRC(b2before['GazePitch']))
A.ix[4,4] = calDTC(b2after['GazeHeading'],b2after['GazePitch'],findRC(b2after['GazeHeading']),findRC(b2after['GazePitch']))
A.ix[4,5] = findRC(b2['GazeHeading'])                      #第六列为事件的水平注视中心
A.ix[4,6] = findRC(b2['GazePitch'])                        #第七列为事件的垂直注视中心
A.ix[4,7] = findRC(b2before['GazeHeading'])                #第8列为接管前水平注视中心
A.ix[4,8] = findRC(b2before['GazePitch'])                  #第9列为接管前垂直注视中心
A.ix[4,9] = findRC(b2after['GazeHeading'])                 #第10列为接管后水平注视中心
A.ix[4,10] = findRC(b2after['GazePitch'])                  #第11列为接管后垂直注视中心
A.ix[4,11] = np.std(b2['GazeHeading'])                      #第12列为事件的水平注视标准差
A.ix[4,12] = np.std(b2['GazePitch'])                        #第13列为事件的垂直注视标准差
A.ix[4,13] = np.std(b2before['GazeHeading'])                #第14列为接管前水平注视标准差
A.ix[4,14] = np.std(b2before['GazePitch'])                  #第15列为接管前垂直注视标准差
A.ix[4,15] = np.std(b2after['GazeHeading'])                 #第16列为接管后水平注视标准差
A.ix[4,16] = np.std(b2after['GazePitch'])                  #第17列为接管后垂直注视标准差

#第6段34km紧急接管
f3TimePoint = float(timepoint['34km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(f3TimePoint-60)]
f3before = temp1[temp1['time']< f3TimePoint]	
temp2 = data[data['time']> f3TimePoint]
f3after = temp2[temp2['time'] < (f3TimePoint + 30)]
f3 = temp1[temp1['time'] < (f3TimePoint + 30)]

A.ix[5,0] = x
A.ix[5,1] = 2
A.ix[5,2] = 1
A.ix[5,3] = calDTC(f3before['GazeHeading'],f3before['GazePitch'],findRC(f3before['GazeHeading']),findRC(f3before['GazePitch']))
A.ix[5,4] = calDTC(f3after['GazeHeading'],f3after['GazePitch'],findRC(f3after['GazeHeading']),findRC(f3after['GazePitch']))
A.ix[5,5] = findRC(f3['GazeHeading'])                      #第六列为事件的水平注视中心
A.ix[5,6] = findRC(f3['GazePitch'])                        #第七列为事件的垂直注视中心
A.ix[5,7] = findRC(f3before['GazeHeading'])                #第8列为接管前水平注视中心
A.ix[5,8] = findRC(f3before['GazePitch'])                  #第9列为接管前垂直注视中心
A.ix[5,9] = findRC(f3after['GazeHeading'])                 #第10列为接管后水平注视中心
A.ix[5,10] = findRC(f3after['GazePitch'])                  #第11列为接管后垂直注视中心
A.ix[5,11] = np.std(f3['GazeHeading'])                      #第12列为事件的水平注视标准差
A.ix[5,12] = np.std(f3['GazePitch'])                        #第13列为事件的垂直注视标准差
A.ix[5,13] = np.std(f3before['GazeHeading'])                #第14列为接管前水平注视标准差
A.ix[5,14] = np.std(f3before['GazePitch'])                  #第15列为接管前垂直注视标准差
A.ix[5,15] = np.std(f3after['GazeHeading'])                 #第16列为接管后水平注视标准差
A.ix[5,16] = np.std(f3after['GazePitch'])                  #第17列为接管后垂直注视标准差


A.columns = ['subject','secondarytask','emergency','before_PRC','after_PRC','EventHeadingCenter','EventPithchCenter','beforeHeadingCenter','beforePitchCenter',
'afterHeadingCenter','afterPitchCenter','EventHeadingSD','EventPithchSD','beforeHeadingSD','beforePitchSD','afterHeadingSD','afterPitchSD']
A.to_csv('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyerecorderdata\\3_PRC\\' + 'PRC_' + x,index = False,)

'''

