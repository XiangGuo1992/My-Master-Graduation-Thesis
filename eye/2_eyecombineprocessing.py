import os
import numpy as np
import pandas as pd
from pandas import read_csv 
import math
from collections import Counter
os.chdir('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyeprolog\\2_fix&sac\\others')              #变更工作目录
#os.chdir('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyeprolog\\2_f&s_alone') 
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


#计算对应次数
def calTimes(s):
	s = s[s.ix [:,1] != 0]
	s1 = pd.Series(Counter(s.ix[:,1]))
	return len(s1[s1 >= 6].index)

#计算平均时长
def MeanTime(s):
	s = s[s.ix [:,1] != 0]
	s1 = pd.Series(Counter(s.ix[:,1]))
	s1_index = s1[s1 >= 6].index
	r = np.empty(len(s1_index))
	for i in range(len(s1_index)):
		section = s['time'][s.ix[:,1]==s1_index[i]]
		r[i] = max(section) - min(section)
	return r.mean()

def MaxTime(s):
	s = s[s.ix [:,1] != 0]
	s1 = pd.Series(Counter(s.ix[:,1]))
	s1_index = s1[s1 >= 6].index
	r = np.empty(len(s1_index))
	for i in range(len(s1_index)):
		section = s['time'][s.ix[:,1]==s1_index[i]]
		r[i] = max(section) - min(section)
	return r.max()

'''
for x in listfile:
	data = read_csv(x)
	#时间修正
	SubjectNum = int(x.split(sep = '.')[0])           #获得被试编号
	data = data[data['GazeDirectionQ']>0.5]
	data['time'] = data['time'] - float(timedelay['StartPoint'][timedelay['Subject']==SubjectNum])
	data = data[data['time']>= 0]
	data.index = range(len(data))
	data['AOI']=np.empty(len(data))
	#单位转化   
	data['GazeHeading'][data['GazeHeading'] > 0] = 180-data['GazeHeading'][data['GazeHeading'] > 0]*180/math.pi
	data['GazeHeading'][data['GazeHeading'] < 0] = -data['GazeHeading'][data['GazeHeading'] < 0]*180/math.pi -180
	data['GazePitch'] = data['GazePitch']*180/math.pi

	#变量A存储PRC值
	A= pd.DataFrame(np.zeros((6,17)))   

	#第一段5km处非紧急接管
	f1TimePoint = float(timepoint['5km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(f1TimePoint-60)]
	f1 = temp1[temp1['time'] < (f1TimePoint + 30)]
	f1['AOI'][((f1['GazeHeading'] - findRC(f1['GazeHeading']))**2 + (f1['GazePitch']-findRC(f1['GazePitch']))**2)**0.5 < 16] = 1
	f1['AOI'][((f1['GazeHeading'] - findRC(f1['GazeHeading']))**2 + (f1['GazePitch']-findRC(f1['GazePitch']))**2)**0.5 >= 16] = 0

	f1before = f1[f1['time']< f1TimePoint]	
	f1after = f1[f1['time'] > f1TimePoint]

	A.ix[0,0] = x
	A.ix[0,1] = 0
	A.ix[0,2] = 0
	A.ix[0,3] = calTimes(f1[['time','Fixation']])           #计算阶段内凝视次数
	A.ix[0,4] = MeanTime(f1[['time','Fixation']])           #阶段内平均凝视时长
	A.ix[0,5] = calTimes(f1[['time','Saccade']])           #计算阶段内扫视次数
	A.ix[0,6] = MeanTime(f1[['time','Saccade']]) 			#阶段内平均扫视时长
	A.ix[0,7] = calTimes(f1before[['time','Fixation']])           #计算接管前前凝视次数
	A.ix[0,8] = MeanTime(f1before[['time','Fixation']])           #接管前平均凝视时长
	A.ix[0,9] = calTimes(f1before[['time','Saccade']])           #计算接管前扫视次数
	A.ix[0,10] = MeanTime(f1before[['time','Saccade']]) 			#接管前平均扫视时长
	A.ix[0,11] = calTimes(f1after[['time','Fixation']])           #计算接管后前凝视次数
	A.ix[0,12] = MeanTime(f1after[['time','Fixation']])           #接管后平均凝视时长
	A.ix[0,13] = calTimes(f1after[['time','Saccade']])           #计算接管后扫视次数
	A.ix[0,14] = MeanTime(f1after[['time','Saccade']]) 			#接管后平均扫视时长
	A.ix[0,15] = MaxTime(f1before[['time','Fixation']])            #接管前最大凝视时长
	A.ix[0,16] = MaxTime(f1before[['time','Saccade']])            #接管前最大扫视时长



	#第二段10km紧急接管
	b1TimePoint = float(timepoint['10km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(b1TimePoint-60)]
	b1 = temp1[temp1['time'] < (b1TimePoint + 30)]


	b1before = b1[b1['time']< b1TimePoint]	
	b1after = b1[b1['time'] > b1TimePoint]

	A.ix[1,0] = x
	A.ix[1,1] = 0
	A.ix[1,2] = 1
	A.ix[1,3] = calTimes(b1[['time','Fixation']])           #计算阶段内凝视次数
	A.ix[1,4] = MeanTime(b1[['time','Fixation']])           #阶段内平均凝视时长
	A.ix[1,5] = calTimes(b1[['time','Saccade']])           #计算阶段内扫视次数
	A.ix[1,6] = MeanTime(b1[['time','Saccade']]) 			#阶段内平均扫视时长
	A.ix[1,7] = calTimes(b1before[['time','Fixation']])           #计算接管前前凝视次数
	A.ix[1,8] = MeanTime(b1before[['time','Fixation']])           #接管前平均凝视时长
	A.ix[1,9] = calTimes(b1before[['time','Saccade']])           #计算接管前扫视次数
	A.ix[1,10] = MeanTime(b1before[['time','Saccade']]) 			#接管前平均扫视时长
	A.ix[1,11] = calTimes(b1after[['time','Fixation']])           #计算接管后前凝视次数
	A.ix[1,12] = MeanTime(b1after[['time','Fixation']])           #接管后平均凝视时长
	A.ix[1,13] = calTimes(b1after[['time','Saccade']])           #计算接管后扫视次数
	A.ix[1,14] = MeanTime(b1after[['time','Saccade']]) 			#接管后平均扫视时长
	A.ix[1,15] = MaxTime(b1before[['time','Fixation']])            #接管前最大凝视时长
	A.ix[1,16] = MaxTime(b1before[['time','Saccade']])            #接管前最大扫视时长

	#第3段17km非紧急接管
	f2TimePoint = float(timepoint['17km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(f2TimePoint-60)]
	f2 = temp1[temp1['time'] < (f2TimePoint + 30)]


	f2before = f2[f2['time']< f2TimePoint]	
	f2after = f2[f2['time'] > f2TimePoint]

	A.ix[2,0] = x
	A.ix[2,1] = 1
	A.ix[2,2] = 0
	A.ix[2,3] = calTimes(f2[['time','Fixation']])           #计算阶段内凝视次数
	A.ix[2,4] = MeanTime(f2[['time','Fixation']])           #阶段内平均凝视时长
	A.ix[2,5] = calTimes(f2[['time','Saccade']])           #计算阶段内扫视次数
	A.ix[2,6] = MeanTime(f2[['time','Saccade']]) 			#阶段内平均扫视时长
	A.ix[2,7] = calTimes(f2before[['time','Fixation']])           #计算接管前前凝视次数
	A.ix[2,8] = MeanTime(f2before[['time','Fixation']])           #接管前平均凝视时长
	A.ix[2,9] = calTimes(f2before[['time','Saccade']])           #计算接管前扫视次数
	A.ix[2,10] = MeanTime(f2before[['time','Saccade']]) 			#接管前平均扫视时长
	A.ix[2,11] = calTimes(f2after[['time','Fixation']])           #计算接管后前凝视次数
	A.ix[2,12] = MeanTime(f2after[['time','Fixation']])           #接管后平均凝视时长
	A.ix[2,13] = calTimes(f2after[['time','Saccade']])           #计算接管后扫视次数
	A.ix[2,14] = MeanTime(f2after[['time','Saccade']]) 			#接管后平均扫视时长
	A.ix[2,15] = MaxTime(f2before[['time','Fixation']])            #接管前最大凝视时长
	A.ix[2,16] = MaxTime(f2before[['time','Saccade']])            #接管前最大扫视时长

	#第4段22km紧急接管
	f2TimePoint2 = float(timepoint['22km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(f2TimePoint2-60)]
	f22 = temp1[temp1['time'] < (f2TimePoint2 + 30)]


	f2before2 = f22[f22['time']< f2TimePoint2]
	f2after2 = f22[f22['time'] > f2TimePoint2]


	A.ix[3,0] = x
	A.ix[3,1] = 1
	A.ix[3,2] = 1
	A.ix[3,3] = calTimes(f22[['time','Fixation']])           #计算阶段内凝视次数
	A.ix[3,4] = MeanTime(f22[['time','Fixation']])           #阶段内平均凝视时长
	A.ix[3,5] = calTimes(f22[['time','Saccade']])           #计算阶段内扫视次数
	A.ix[3,6] = MeanTime(f22[['time','Saccade']]) 			#阶段内平均扫视时长
	A.ix[3,7] = calTimes(f2before2[['time','Fixation']])           #计算接管前前凝视次数
	A.ix[3,8] = MeanTime(f2before2[['time','Fixation']])           #接管前平均凝视时长
	A.ix[3,9] = calTimes(f2before2[['time','Saccade']])           #计算接管前扫视次数
	A.ix[3,10] = MeanTime(f2before2[['time','Saccade']]) 			#接管前平均扫视时长
	A.ix[3,11] = calTimes(f2after2[['time','Fixation']])           #计算接管后前凝视次数
	A.ix[3,12] = MeanTime(f2after2[['time','Fixation']])           #接管后平均凝视时长
	A.ix[3,13] = calTimes(f2after2[['time','Saccade']])           #计算接管后扫视次数
	A.ix[3,14] = MeanTime(f2after2[['time','Saccade']]) 			#接管后平均扫视时长
	A.ix[3,15] = MaxTime(f2before2[['time','Fixation']])            #接管前最大凝视时长
	A.ix[3,16] = MaxTime(f2before2[['time','Saccade']])            #接管前最大扫视时长

	#第5段29km非紧急接管
	b2TimePoint = float(timepoint['29km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(b2TimePoint-60)]
	b2 = temp1[temp1['time'] < (b2TimePoint + 30)]


	b2before = b2[b2['time']< b2TimePoint]	
	b2after = b2[b2['time'] > b2TimePoint]

	A.ix[4,0] = x
	A.ix[4,1] = 2
	A.ix[4,2] = 0
	A.ix[4,3] = calTimes(b2[['time','Fixation']])           #计算阶段内凝视次数
	A.ix[4,4] = MeanTime(b2[['time','Fixation']])           #阶段内平均凝视时长
	A.ix[4,5] = calTimes(b2[['time','Saccade']])           #计算阶段内扫视次数
	A.ix[4,6] = MeanTime(b2[['time','Saccade']]) 			#阶段内平均扫视时长
	A.ix[4,7] = calTimes(b2before[['time','Fixation']])           #计算接管前前凝视次数
	A.ix[4,8] = MeanTime(b2before[['time','Fixation']])           #接管前平均凝视时长
	A.ix[4,9] = calTimes(b2before[['time','Saccade']])           #计算接管前扫视次数
	A.ix[4,10] = MeanTime(b2before[['time','Saccade']]) 			#接管前平均扫视时长
	A.ix[4,11] = calTimes(b2after[['time','Fixation']])           #计算接管后前凝视次数
	A.ix[4,12] = MeanTime(b2after[['time','Fixation']])           #接管后平均凝视时长
	A.ix[4,13] = calTimes(b2after[['time','Saccade']])           #计算接管后扫视次数
	A.ix[4,14] = MeanTime(b2after[['time','Saccade']]) 			#接管后平均扫视时长
	A.ix[4,15] = MaxTime(b2before[['time','Fixation']])            #接管前最大凝视时长
	A.ix[4,16] = MaxTime(b2before[['time','Saccade']])            #接管前最大扫视时长


	#第6段34km紧急接管
	f3TimePoint = float(timepoint['34km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(f3TimePoint-60)]
	f3 = temp1[temp1['time'] < (f3TimePoint + 30)]


	f3before = f3[f3['time']< f3TimePoint]	
	f3after = f3[f3['time'] > f3TimePoint]

	A.ix[5,0] = x
	A.ix[5,1] = 2
	A.ix[5,2] = 1
	A.ix[5,3] = calTimes(f3[['time','Fixation']])           #计算阶段内凝视次数
	A.ix[5,4] = MeanTime(f3[['time','Fixation']])           #阶段内平均凝视时长
	A.ix[5,5] = calTimes(f3[['time','Saccade']])           #计算阶段内扫视次数
	A.ix[5,6] = MeanTime(f3[['time','Saccade']]) 			#阶段内平均扫视时长
	A.ix[5,7] = calTimes(f3before[['time','Fixation']])           #计算接管前前凝视次数
	A.ix[5,8] = MeanTime(f3before[['time','Fixation']])           #接管前平均凝视时长
	A.ix[5,9] = calTimes(f3before[['time','Saccade']])           #计算接管前扫视次数
	A.ix[5,10] = MeanTime(f3before[['time','Saccade']]) 			#接管前平均扫视时长
	A.ix[5,11] = calTimes(f3after[['time','Fixation']])           #计算接管后前凝视次数
	A.ix[5,12] = MeanTime(f3after[['time','Fixation']])           #接管后平均凝视时长
	A.ix[5,13] = calTimes(f3after[['time','Saccade']])           #计算接管后扫视次数
	A.ix[5,14] = MeanTime(f3after[['time','Saccade']]) 			#接管后平均扫视时长
	A.ix[5,15] = MaxTime(f3before[['time','Fixation']])            #接管前最大凝视时长
	A.ix[5,16] = MaxTime(f3before[['time','Saccade']])            #接管前最大扫视时长


	A.columns = ['subject','secondarytask','emergency','fix_times','fix_length','sac_times','sac_length','fix_times_before','fix_length_before','sac_times_before','sac_length_before','fix_times_after','fix_length_after','sac_times_after','sac_length_after','fix_max_before','sac_max_before']
	A.to_csv('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyeprolog\\3_Tf&Ts\\' + x,index = False)
	

'''
x='213.csv'
data = read_csv(x)
#时间修正
SubjectNum = int(x.split(sep = '.')[0])           #获得被试编号
data = data[data['GazeDirectionQ']>0.5]
data['time'] = data['time'] - float(timedelay['StartPoint'][timedelay['Subject']==SubjectNum])
data = data[data['time']>= 0]
data.index = range(len(data))
data['AOI']=np.empty(len(data))
#单位转化   
data['GazeHeading'][data['GazeHeading'] > 0] = 180-data['GazeHeading'][data['GazeHeading'] > 0]*180/math.pi
data['GazeHeading'][data['GazeHeading'] < 0] = -data['GazeHeading'][data['GazeHeading'] < 0]*180/math.pi -180
data['GazePitch'] = data['GazePitch']*180/math.pi

#变量A存储PRC值
A= pd.DataFrame(np.zeros((6,17)))   


#第一段5km处非紧急接管
f1TimePoint = float(timepoint['5km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(f1TimePoint-60)]
f1 = temp1[temp1['time'] < (f1TimePoint + 30)]
f1['AOI'][((f1['GazeHeading'] - findRC(f1['GazeHeading']))**2 + (f1['GazePitch']-findRC(f1['GazePitch']))**2)**0.5 < 16] = 1
f1['AOI'][((f1['GazeHeading'] - findRC(f1['GazeHeading']))**2 + (f1['GazePitch']-findRC(f1['GazePitch']))**2)**0.5 >= 16] = 0

f1before = f1[f1['time']< f1TimePoint]	
f1after = f1[f1['time'] > f1TimePoint]

A.ix[0,0] = x
A.ix[0,1] = 0
A.ix[0,2] = 0
A.ix[0,3] = calTimes(f1[['time','Fixation']])           #计算阶段内凝视次数
A.ix[0,4] = MeanTime(f1[['time','Fixation']])           #阶段内平均凝视时长
A.ix[0,5] = calTimes(f1[['time','Saccade']])           #计算阶段内扫视次数
A.ix[0,6] = MeanTime(f1[['time','Saccade']]) 			#阶段内平均扫视时长
A.ix[0,7] = calTimes(f1before[['time','Fixation']])           #计算接管前前凝视次数
A.ix[0,8] = MeanTime(f1before[['time','Fixation']])           #接管前平均凝视时长
A.ix[0,9] = calTimes(f1before[['time','Saccade']])           #计算接管前扫视次数
A.ix[0,10] = MeanTime(f1before[['time','Saccade']]) 			#接管前平均扫视时长
A.ix[0,11] = calTimes(f1after[['time','Fixation']])           #计算接管后前凝视次数
A.ix[0,12] = MeanTime(f1after[['time','Fixation']])           #接管后平均凝视时长
A.ix[0,13] = calTimes(f1after[['time','Saccade']])           #计算接管后扫视次数
A.ix[0,14] = MeanTime(f1after[['time','Saccade']]) 			#接管后平均扫视时长
A.ix[0,15] = MaxTime(f1before[['time','Fixation']])            #接管前最大凝视时长
A.ix[0,16] = MaxTime(f1before[['time','Saccade']])            #接管前最大扫视时长



#第二段10km紧急接管
b1TimePoint = float(timepoint['10km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(b1TimePoint-60)]
b1 = temp1[temp1['time'] < (b1TimePoint + 30)]
b1['AOI'][((b1['GazeHeading'] - findRC(b1['GazeHeading']))**2 + (b1['GazePitch']-findRC(b1['GazePitch']))**2)**0.5 < 16] = 1
b1['AOI'][((b1['GazeHeading'] - findRC(b1['GazeHeading']))**2 + (b1['GazePitch']-findRC(b1['GazePitch']))**2)**0.5 >= 16] = 0

b1before = b1[b1['time']< b1TimePoint]	
b1after = b1[b1['time'] > b1TimePoint]

A.ix[1,0] = x
A.ix[1,1] = 0
A.ix[1,2] = 1
A.ix[1,3] = calTimes(b1[['time','Fixation']])           #计算阶段内凝视次数
A.ix[1,4] = MeanTime(b1[['time','Fixation']])           #阶段内平均凝视时长
A.ix[1,5] = calTimes(b1[['time','Saccade']])           #计算阶段内扫视次数
A.ix[1,6] = MeanTime(b1[['time','Saccade']]) 			#阶段内平均扫视时长
A.ix[1,7] = calTimes(b1before[['time','Fixation']])           #计算接管前前凝视次数
A.ix[1,8] = MeanTime(b1before[['time','Fixation']])           #接管前平均凝视时长
A.ix[1,9] = calTimes(b1before[['time','Saccade']])           #计算接管前扫视次数
A.ix[1,10] = MeanTime(b1before[['time','Saccade']]) 			#接管前平均扫视时长
A.ix[1,11] = calTimes(b1after[['time','Fixation']])           #计算接管后前凝视次数
A.ix[1,12] = MeanTime(b1after[['time','Fixation']])           #接管后平均凝视时长
A.ix[1,13] = calTimes(b1after[['time','Saccade']])           #计算接管后扫视次数
A.ix[1,14] = MeanTime(b1after[['time','Saccade']]) 			#接管后平均扫视时长
A.ix[1,15] = MaxTime(b1before[['time','Fixation']])            #接管前最大凝视时长
A.ix[1,16] = MaxTime(b1before[['time','Saccade']])            #接管前最大扫视时长



#第3段17km非紧急接管
f2TimePoint = float(timepoint['17km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(f2TimePoint-60)]
f2 = temp1[temp1['time'] < (f2TimePoint + 30)]
f2['AOI'][((f2['GazeHeading'] - findRC(f2['GazeHeading']))**2 + (f2['GazePitch']-findRC(f2['GazePitch']))**2)**0.5 < 16] = 1
f2['AOI'][((f2['GazeHeading'] - findRC(f2['GazeHeading']))**2 + (f2['GazePitch']-findRC(f2['GazePitch']))**2)**0.5 >= 16] = 0

f2before = f2[f2['time']< f2TimePoint]	
f2after = f2[f2['time'] > f2TimePoint]

A.ix[2,0] = x
A.ix[2,1] = 1
A.ix[2,2] = 0
A.ix[2,3] = calTimes(f2[['time','Fixation']])           #计算阶段内凝视次数
A.ix[2,4] = MeanTime(f2[['time','Fixation']])           #阶段内平均凝视时长
A.ix[2,5] = calTimes(f2[['time','Saccade']])           #计算阶段内扫视次数
A.ix[2,6] = MeanTime(f2[['time','Saccade']]) 			#阶段内平均扫视时长
A.ix[2,7] = calTimes(f2before[['time','Fixation']])           #计算接管前前凝视次数
A.ix[2,8] = MeanTime(f2before[['time','Fixation']])           #接管前平均凝视时长
A.ix[2,9] = calTimes(f2before[['time','Saccade']])           #计算接管前扫视次数
A.ix[2,10] = MeanTime(f2before[['time','Saccade']]) 			#接管前平均扫视时长
A.ix[2,11] = calTimes(f2after[['time','Fixation']])           #计算接管后前凝视次数
A.ix[2,12] = MeanTime(f2after[['time','Fixation']])           #接管后平均凝视时长
A.ix[2,13] = calTimes(f2after[['time','Saccade']])           #计算接管后扫视次数
A.ix[2,14] = MeanTime(f2after[['time','Saccade']]) 			#接管后平均扫视时长
A.ix[2,15] = MaxTime(f2before[['time','Fixation']])            #接管前最大凝视时长
A.ix[2,16] = MaxTime(f2before[['time','Saccade']])            #接管前最大扫视时长


#第4段22km紧急接管
f2TimePoint2 = float(timepoint['22km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(f2TimePoint2-60)]
f22 = temp1[temp1['time'] < (f2TimePoint2 + 30)]
f22['AOI'][((f22['GazeHeading'] - findRC(f22['GazeHeading']))**2 + (f22['GazePitch']-findRC(f22['GazePitch']))**2)**0.5 < 16] = 1
f22['AOI'][((f22['GazeHeading'] - findRC(f22['GazeHeading']))**2 + (f22['GazePitch']-findRC(f22['GazePitch']))**2)**0.5 >= 16] = 0

f2before2 = f22[f22['time']< f2TimePoint2]
f2after2 = f22[f22['time'] > f2TimePoint2]


A.ix[3,0] = x
A.ix[3,1] = 1
A.ix[3,2] = 1
A.ix[3,3] = calTimes(f22[['time','Fixation']])           #计算阶段内凝视次数
A.ix[3,4] = MeanTime(f22[['time','Fixation']])           #阶段内平均凝视时长
A.ix[3,5] = calTimes(f22[['time','Saccade']])           #计算阶段内扫视次数
A.ix[3,6] = MeanTime(f22[['time','Saccade']]) 			#阶段内平均扫视时长
A.ix[3,7] = calTimes(f2before2[['time','Fixation']])           #计算接管前前凝视次数
A.ix[3,8] = MeanTime(f2before2[['time','Fixation']])           #接管前平均凝视时长
A.ix[3,9] = calTimes(f2before2[['time','Saccade']])           #计算接管前扫视次数
A.ix[3,10] = MeanTime(f2before2[['time','Saccade']]) 			#接管前平均扫视时长
A.ix[3,11] = calTimes(f2after2[['time','Fixation']])           #计算接管后前凝视次数
A.ix[3,12] = MeanTime(f2after2[['time','Fixation']])           #接管后平均凝视时长
A.ix[3,13] = calTimes(f2after2[['time','Saccade']])           #计算接管后扫视次数
A.ix[3,14] = MeanTime(f2after2[['time','Saccade']]) 			#接管后平均扫视时长
A.ix[3,15] = MaxTime(f2before2[['time','Fixation']])            #接管前最大凝视时长
A.ix[3,16] = MaxTime(f2before2[['time','Saccade']])            #接管前最大扫视时长




#第5段29km非紧急接管
b2TimePoint = float(timepoint['29km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(b2TimePoint-60)]
b2 = temp1[temp1['time'] < (b2TimePoint + 30)]
b2['AOI'][((b2['GazeHeading'] - findRC(b2['GazeHeading']))**2 + (b2['GazePitch']-findRC(b2['GazePitch']))**2)**0.5 < 16] = 1
b2['AOI'][((b2['GazeHeading'] - findRC(b2['GazeHeading']))**2 + (b2['GazePitch']-findRC(b2['GazePitch']))**2)**0.5 >= 16] = 0

b2before = b2[b2['time']< b2TimePoint]	
b2after = b2[b2['time'] > b2TimePoint]

A.ix[4,0] = x
A.ix[4,1] = 2
A.ix[4,2] = 0
A.ix[4,3] = calTimes(b2[['time','Fixation']])           #计算阶段内凝视次数
A.ix[4,4] = MeanTime(b2[['time','Fixation']])           #阶段内平均凝视时长
A.ix[4,5] = calTimes(b2[['time','Saccade']])           #计算阶段内扫视次数
A.ix[4,6] = MeanTime(b2[['time','Saccade']]) 			#阶段内平均扫视时长
A.ix[4,7] = calTimes(b2before[['time','Fixation']])           #计算接管前前凝视次数
A.ix[4,8] = MeanTime(b2before[['time','Fixation']])           #接管前平均凝视时长
A.ix[4,9] = calTimes(b2before[['time','Saccade']])           #计算接管前扫视次数
A.ix[4,10] = MeanTime(b2before[['time','Saccade']]) 			#接管前平均扫视时长
A.ix[4,11] = calTimes(b2after[['time','Fixation']])           #计算接管后前凝视次数
A.ix[4,12] = MeanTime(b2after[['time','Fixation']])           #接管后平均凝视时长
A.ix[4,13] = calTimes(b2after[['time','Saccade']])           #计算接管后扫视次数
A.ix[4,14] = MeanTime(b2after[['time','Saccade']]) 			#接管后平均扫视时长
A.ix[4,15] = MaxTime(b2before[['time','Fixation']])            #接管前最大凝视时长
A.ix[4,16] = MaxTime(b2before[['time','Saccade']])            #接管前最大扫视时长


#第6段34km紧急接管
f3TimePoint = float(timepoint['34km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(f3TimePoint-60)]
f3 = temp1[temp1['time'] < (f3TimePoint + 30)]
f3['AOI'][((f3['GazeHeading'] - findRC(f3['GazeHeading']))**2 + (f3['GazePitch']-findRC(f3['GazePitch']))**2)**0.5 < 16] = 1
f3['AOI'][((f3['GazeHeading'] - findRC(f3['GazeHeading']))**2 + (f3['GazePitch']-findRC(f3['GazePitch']))**2)**0.5 >= 16] = 0

f3before = f3[f3['time']< f3TimePoint]	
f3after = f3[f3['time'] > f3TimePoint]

A.ix[5,0] = x
A.ix[5,1] = 2
A.ix[5,2] = 1
A.ix[5,3] = calTimes(f3[['time','Fixation']])           #计算阶段内凝视次数
A.ix[5,4] = MeanTime(f3[['time','Fixation']])           #阶段内平均凝视时长
A.ix[5,5] = calTimes(f3[['time','Saccade']])           #计算阶段内扫视次数
A.ix[5,6] = MeanTime(f3[['time','Saccade']]) 			#阶段内平均扫视时长
A.ix[5,7] = calTimes(f3before[['time','Fixation']])           #计算接管前前凝视次数
A.ix[5,8] = MeanTime(f3before[['time','Fixation']])           #接管前平均凝视时长
A.ix[5,9] = calTimes(f3before[['time','Saccade']])           #计算接管前扫视次数
A.ix[5,10] = MeanTime(f3before[['time','Saccade']]) 			#接管前平均扫视时长
A.ix[5,11] = calTimes(f3after[['time','Fixation']])           #计算接管后前凝视次数
A.ix[5,12] = MeanTime(f3after[['time','Fixation']])           #接管后平均凝视时长
A.ix[5,13] = calTimes(f3after[['time','Saccade']])           #计算接管后扫视次数
A.ix[5,14] = MeanTime(f3after[['time','Saccade']]) 			#接管后平均扫视时长
A.ix[5,15] = MaxTime(f3before[['time','Fixation']])            #接管前最大凝视时长
A.ix[5,16] = MaxTime(f3before[['time','Saccade']])            #接管前最大扫视时长


A.columns = ['subject','secondarytask','emergency','fix_times','fix_length','sac_times','sac_length','fix_times_before','fix_length_before','sac_times_before','sac_length_before','fix_times_after','fix_length_after','sac_times_after','sac_length_after','fix_max_before','sac_max_before']
A.to_csv('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyeprolog\\3_Tf&Ts\\' + x,index = False,)
