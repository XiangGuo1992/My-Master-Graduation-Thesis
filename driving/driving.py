# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 18:57:16 2016

@author: sqc
"""

import os
import numpy as np
import pandas as pd
from pandas import read_csv 
os.chdir('F:\\GuoXiang\\硕士毕业论文\\DATA\\data\\1_rawdata')              #变更工作目录
listfile = os.listdir()                                             #列出所有文件
print (listfile)



for x in listfile:    #批量处理
	drivingdata = read_csv(x)  #读取文件
	filtercol = ['Time','speedInKmPerHour','speedInMetresPerSecond','distanceTravelled',
               'steering','steeringVelocity','turningCurvature','throttle'
               ,'brake','lightState','distanceAlongRoad','distanceToLeftBorder','distanceToRightBorder','offsetFromRoadCenter'
               ,'offsetFromLaneCenter','laneNumber','laneWidth','laneCurvature','drivingForwards']
	A = drivingdata[(drivingdata['Type']=='uv') & (drivingdata["Time"] >0)][filtercol]
	A['Time']= A['Time']-A['Time'][1]
	filename = 'F:\\GuoXiang\\硕士毕业论文\\DATA\\data\\2_filterdata\\' + x.split(sep = '.')[0] + '.csv'     #保存的文件名定义 
	A.to_csv(filename,index = False)                    #输出.csv文件		       



                                             

	


     
 