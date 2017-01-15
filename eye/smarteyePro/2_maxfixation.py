import os
import numpy as np
import pandas as pd
from pandas import read_csv 
import math
from collections import Counter
#os.chdir('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyeprolog\\2_fix&sac')              #变更工作目录
os.chdir('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyeprolog\\2_f&s_alone') 
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


	#单位转化   
	data['GazeHeading'][data['GazeHeading'] > 0] = 180-data['GazeHeading'][data['GazeHeading'] > 0]*180/math.pi
	data['GazeHeading'][data['GazeHeading'] < 0] = -data['GazeHeading'][data['GazeHeading'] < 0]*180/math.pi -180
	data['GazePitch'] = data['GazePitch']*180/math.pi

	data['AOI']=np.empty(len(data))
	data['AOI'][((data['GazeHeading'] - findRC(data['GazeHeading']))**2 + (data['GazePitch']-findRC(data['GazePitch']))**2)**0.5 < 16] = 1
	data['AOI'][((data['GazeHeading'] - findRC(data['GazeHeading']))**2 + (data['GazePitch']-findRC(data['GazePitch']))**2)**0.5 >= 16] = 0

	#变量A存储PRC值
	A= pd.DataFrame(np.zeros((6,6)))   
	A.ix[0,0] = x
	A.ix[0,1] = 0
	A.ix[0,2] = 0
	A.ix[1,0] = x
	A.ix[1,1] = 0
	A.ix[1,2] = 1
	A.ix[2,0] = x
	A.ix[2,1] = 1
	A.ix[2,2] = 0	
	A.ix[3,0] = x
	A.ix[3,1] = 1
	A.ix[3,2] = 1
	A.ix[4,0] = x
	A.ix[4,1] = 2
	A.ix[4,2] = 0
	A.ix[5,0] = x
	A.ix[5,1] = 2
	A.ix[5,2] = 1

	#第一段5km处非紧急接管
	f1TimePoint = float(timepoint['5km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(f1TimePoint-60)]
	f1 = temp1[temp1['time'] < (f1TimePoint + 30)]

	f1before = f1[f1['time']< f1TimePoint]	
	f1after = f1[f1['time'] > f1TimePoint]

	f1center_before = f1before[f1before['AOI'] == 1]
	f1other_before = f1before[f1before['AOI'] == 0]


	A.ix[0,3] = MaxTime(f1before[['time','Fixation']])            #接管前最大扫视时长
	A.ix[0,4] = MaxTime(f1center_before[['time','Fixation']])		#接管前中心最大扫视长
	A.ix[0,5] = MaxTime(f1other_before[['time','Fixation']])		#接管前非中心最大扫视长




	#第二段10km紧急接管
	b1TimePoint = float(timepoint['10km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(b1TimePoint-60)]
	b1 = temp1[temp1['time'] < (b1TimePoint + 30)]



	b1before = b1[b1['time']< b1TimePoint]	
	b1after = b1[b1['time'] > b1TimePoint]

	b1center_before = b1before[b1before['AOI'] == 1]
	b1other_before = b1before[b1before['AOI'] == 0]


	A.ix[1,3] = MaxTime(b1before[['time','Fixation']])            #接管前最大扫视时长
	A.ix[1,4] = MaxTime(b1center_before[['time','Fixation']])		#接管前中心最大扫视长
	A.ix[1,5] = MaxTime(b1other_before[['time','Fixation']])		#接管前非中心最大扫视长


	#第3段17km非紧急接管
	f2TimePoint = float(timepoint['17km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(f2TimePoint-60)]
	f2 = temp1[temp1['time'] < (f2TimePoint + 30)]


	f2before = f2[f2['time']< f2TimePoint]	
	f2after = f2[f2['time'] > f2TimePoint]

	f2center_before = f2before[f2before['AOI'] == 1]
	f2other_before = f2before[f2before['AOI'] == 0]



	A.ix[2,3] = MaxTime(f2before[['time','Fixation']])            #接管前最大扫视时长
	A.ix[2,4] = MaxTime(f2center_before[['time','Fixation']])		#接管前中心最大扫视长
	A.ix[2,5] = MaxTime(f2other_before[['time','Fixation']])		#接管前非中心最大扫视长




	#第4段22km紧急接管
	f2TimePoint2 = float(timepoint['22km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(f2TimePoint2-60)]
	f22 = temp1[temp1['time'] < (f2TimePoint2 + 30)]


	f2before2 = f22[f22['time']< f2TimePoint2]
	f2after2 = f22[f22['time'] > f2TimePoint2]

	f2center2_before = f2before2[f2before2['AOI'] == 1]
	f2other2_before = f2before2[f2before2['AOI'] == 0]


	A.ix[3,3] = MaxTime(f2before2[['time','Fixation']])            #接管前最大扫视时长
	A.ix[3,4] = MaxTime(f2center2_before[['time','Fixation']])		#接管前中心最大扫视长
	A.ix[3,5] = MaxTime(f2other2_before[['time','Fixation']])		#接管前非中心最大扫视长




	#第5段29km非紧急接管
	b2TimePoint = float(timepoint['29km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(b2TimePoint-60)]
	b2 = temp1[temp1['time'] < (b2TimePoint + 30)]


	b2before = b2[b2['time']< b2TimePoint]	
	b2after = b2[b2['time'] > b2TimePoint]

	b2center_before = b2before[b2before['AOI'] == 1]
	b2other_before = b2before[b2before['AOI'] == 0]


	A.ix[4,3] = MaxTime(b2before[['time','Fixation']])            #接管前最大扫视时长
	A.ix[4,4] = MaxTime(b2center_before[['time','Fixation']])		#接管前中心最大扫视长
	A.ix[4,5] = MaxTime(b2other_before[['time','Fixation']])		#接管前非中心最大扫视长



	#第6段34km紧急接管
	f3TimePoint = float(timepoint['34km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
	temp1 = data[data['time']>(f3TimePoint-60)]
	f3 = temp1[temp1['time'] < (f3TimePoint + 30)]

	f3before = f3[f3['time']< f3TimePoint]	
	f3after = f3[f3['time'] > f3TimePoint]

	f3center_before = f3before[f3before['AOI'] == 1]
	f3other_before = f3before[f3before['AOI'] == 0]


	A.ix[5,3] = MaxTime(f3before[['time','Fixation']])            #接管前最大扫视时长
	A.ix[5,4] = MaxTime(f3center_before[['time','Fixation']])		#接管前中心最大扫视长
	A.ix[5,5] = MaxTime(f3other_before[['time','Fixation']])		#接管前非中心最大扫视长


	A.columns = ['subject','secondarytask','emergency','fix_max_before','fix_center_max_before','fix_other_max_before']
	A.to_csv('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyeprolog\\3_maxfixation\\' + x,index = False)
	

'''
x='409.csv'
data = read_csv(x)
#时间修正
SubjectNum = int(x.split(sep = '.')[0])           #获得被试编号
data = data[data['GazeDirectionQ']>0.5]
data['time'] = data['time'] - float(timedelay['StartPoint'][timedelay['Subject']==SubjectNum])
data = data[data['time']>= 0]
data.index = range(len(data))


#单位转化   
data['GazeHeading'][data['GazeHeading'] > 0] = 180-data['GazeHeading'][data['GazeHeading'] > 0]*180/math.pi
data['GazeHeading'][data['GazeHeading'] < 0] = -data['GazeHeading'][data['GazeHeading'] < 0]*180/math.pi -180
data['GazePitch'] = data['GazePitch']*180/math.pi

data['AOI']=np.empty(len(data))
data['AOI'][((data['GazeHeading'] - findRC(data['GazeHeading']))**2 + (data['GazePitch']-findRC(data['GazePitch']))**2)**0.5 < 16] = 1
data['AOI'][((data['GazeHeading'] - findRC(data['GazeHeading']))**2 + (data['GazePitch']-findRC(data['GazePitch']))**2)**0.5 >= 16] = 0

#变量A存储PRC值
A= pd.DataFrame(np.zeros((6,6)))   
A.ix[0,0] = x
A.ix[0,1] = 0
A.ix[0,2] = 0
A.ix[1,0] = x
A.ix[1,1] = 0
A.ix[1,2] = 1
A.ix[2,0] = x
A.ix[2,1] = 1
A.ix[2,2] = 0	
A.ix[3,0] = x
A.ix[3,1] = 1
A.ix[3,2] = 1
A.ix[4,0] = x
A.ix[4,1] = 2
A.ix[4,2] = 0
A.ix[5,0] = x
A.ix[5,1] = 2
A.ix[5,2] = 1


#第一段5km处非紧急接管
f1TimePoint = float(timepoint['5km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(f1TimePoint-60)]
f1 = temp1[temp1['time'] < (f1TimePoint + 30)]

f1before = f1[f1['time']< f1TimePoint]	
f1after = f1[f1['time'] > f1TimePoint]

f1center_before = f1before[f1before['AOI'] == 1]
f1other_before = f1before[f1before['AOI'] == 0]


A.ix[0,3] = MaxTime(f1before[['time','Fixation']])            #接管前最大扫视时长
A.ix[0,4] = MaxTime(f1center_before[['time','Fixation']])		#接管前中心最大扫视长
A.ix[0,5] = MaxTime(f1other_before[['time','Fixation']])		#接管前非中心最大扫视长




#第二段10km紧急接管
b1TimePoint = float(timepoint['10km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(b1TimePoint-60)]
b1 = temp1[temp1['time'] < (b1TimePoint + 30)]



b1before = b1[b1['time']< b1TimePoint]	
b1after = b1[b1['time'] > b1TimePoint]

b1center_before = b1before[b1before['AOI'] == 1]
b1other_before = b1before[b1before['AOI'] == 0]


A.ix[1,3] = MaxTime(b1before[['time','Fixation']])            #接管前最大扫视时长
A.ix[1,4] = MaxTime(b1center_before[['time','Fixation']])		#接管前中心最大扫视长
A.ix[1,5] = MaxTime(b1other_before[['time','Fixation']])		#接管前非中心最大扫视长


#第3段17km非紧急接管
f2TimePoint = float(timepoint['17km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(f2TimePoint-60)]
f2 = temp1[temp1['time'] < (f2TimePoint + 30)]


f2before = f2[f2['time']< f2TimePoint]	
f2after = f2[f2['time'] > f2TimePoint]

f2center_before = f2before[f2before['AOI'] == 1]
f2other_before = f2before[f2before['AOI'] == 0]



A.ix[2,3] = MaxTime(f2before[['time','Fixation']])            #接管前最大扫视时长
A.ix[2,4] = MaxTime(f2center_before[['time','Fixation']])		#接管前中心最大扫视长
A.ix[2,5] = MaxTime(f2other_before[['time','Fixation']])		#接管前非中心最大扫视长



#第4段22km紧急接管
f2TimePoint2 = float(timepoint['22km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(f2TimePoint2-60)]
f22 = temp1[temp1['time'] < (f2TimePoint2 + 30)]


f2before2 = f22[f22['time']< f2TimePoint2]
f2after2 = f22[f22['time'] > f2TimePoint2]

f2center2_before = f2before2[f2before2['AOI'] == 1]
f2other2_before = f2before2[f2before2['AOI'] == 0]


A.ix[3,3] = MaxTime(f2before2[['time','Fixation']])            #接管前最大扫视时长
A.ix[3,4] = MaxTime(f2center2_before[['time','Fixation']])		#接管前中心最大扫视长
A.ix[3,5] = MaxTime(f2other2_before[['time','Fixation']])		#接管前非中心最大扫视长



#第5段29km非紧急接管
b2TimePoint = float(timepoint['29km非紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(b2TimePoint-60)]
b2 = temp1[temp1['time'] < (b2TimePoint + 30)]


b2before = b2[b2['time']< b2TimePoint]	
b2after = b2[b2['time'] > b2TimePoint]

b2center_before = b2before[b2before['AOI'] == 1]
b2other_before = b2before[b2before['AOI'] == 0]


A.ix[4,3] = MaxTime(b2before[['time','Fixation']])            #接管前最大扫视时长
A.ix[4,4] = MaxTime(b2center_before[['time','Fixation']])		#接管前中心最大扫视长
A.ix[4,5] = MaxTime(b2other_before[['time','Fixation']])		#接管前非中心最大扫视长



#第6段34km紧急接管
f3TimePoint = float(timepoint['34km紧急'][timepoint['subject']==int(x.split(sep = '.')[0])])
temp1 = data[data['time']>(f3TimePoint-60)]
f3 = temp1[temp1['time'] < (f3TimePoint + 30)]

f3before = f3[f3['time']< f3TimePoint]	
f3after = f3[f3['time'] > f3TimePoint]

f3center_before = f3before[f3before['AOI'] == 1]
f3other_before = f3before[f3before['AOI'] == 0]


A.ix[5,3] = MaxTime(f3before[['time','Fixation']])            #接管前最大扫视时长
A.ix[5,4] = MaxTime(f3center_before[['time','Fixation']])		#接管前中心最大扫视长
A.ix[5,5] = MaxTime(f3other_before[['time','Fixation']])		#接管前非中心最大扫视长


A.columns = ['subject','secondarytask','emergency','fix_max_before','fix_center_max_before','fix_other_max_before']
A.to_csv('F:\\GuoXiang\\硕士毕业论文\\DATA\\eye\\eyeprolog\\3_maxfixation\\' + x,index = False)
