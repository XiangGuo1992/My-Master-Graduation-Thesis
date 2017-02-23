# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 11:30:20 2017

@author: gusiev
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

from pybrain.datasets import ClassificationDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer, LinearLayer, SigmoidLayer, SoftmaxLayer
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities import percentError

os.chdir('F:\\GuoXiang\\硕士毕业论文\\DATA\\result\\模型')              #变更工作目录 
data = pd.read_csv('collision模型.csv',encoding='gbk')  #读取文件

features1 = ['secondarytask','因子1_认知错误','sd_steering','sd_steeringVelocity','sd_laneposition',
'mean_steering_before','mean_steeringVelocity_before','sd_laneposition_before','turningCurve_before',
'laneCurve_before','sd_laneCurve_before','HR_sd_after','sac_times_after','是否碰撞']  #完整显著的特征
features2 = ['secondarytask','因子1_认知错误','sd_steering','sd_steeringVelocity','sd_laneposition',
'mean_steering_before','mean_steeringVelocity_before','sd_laneposition_before','turningCurve_before',
'laneCurve_before','sd_laneCurve_before','HR_sd_after','是否碰撞']  #无眼动的特征
features3 = ['secondarytask','因子1_认知错误','sd_steering','sd_steeringVelocity','sd_laneposition',
'mean_steering_before','mean_steeringVelocity_before','sd_laneposition_before','turningCurve_before',
'laneCurve_before','sd_laneCurve_before','sac_times_after','是否碰撞']  #无生理的特征
features4 = ['secondarytask','sd_steering','sd_steeringVelocity','sd_laneposition',
'mean_steering_before','mean_steeringVelocity_before','sd_laneposition_before','turningCurve_before',
'laneCurve_before','sd_laneCurve_before','HR_sd_after','sac_times_after','是否碰撞']  #无因子的特征
features5 = ['secondarytask','因子1_认知错误','sd_steering','sd_steeringVelocity','sd_laneposition',
'mean_steering_before','mean_steeringVelocity_before','sd_laneposition_before','turningCurve_before',
'laneCurve_before','sd_laneCurve_before','是否碰撞']  #无眼动生理的特征
features6 = ['secondarytask','sd_steering','sd_steeringVelocity','sd_laneposition',
'mean_steering_before','mean_steeringVelocity_before','sd_laneposition_before','turningCurve_before',
'laneCurve_before','sd_laneCurve_before','HR_sd_after','是否碰撞']  #无眼动因子的特征
features7 = ['secondarytask','sd_steering','sd_steeringVelocity','sd_laneposition',
'mean_steering_before','mean_steeringVelocity_before','sd_laneposition_before','turningCurve_before',
'laneCurve_before','sd_laneCurve_before','sac_times_after','是否碰撞']  #无生理因子的特征
features8 = ['secondarytask','sd_steering','sd_steeringVelocity','sd_laneposition',
'mean_steering_before','mean_steeringVelocity_before','sd_laneposition_before','turningCurve_before',
'laneCurve_before','sd_laneCurve_before','是否碰撞']  #纯驾驶特征有次任务
features9 = ['sd_steering','sd_steeringVelocity','sd_laneposition',
'mean_steering_before','mean_steeringVelocity_before','sd_laneposition_before','turningCurve_before',
'laneCurve_before','sd_laneCurve_before','是否碰撞']  #纯驾驶特征
features10 = ['secondarytask','因子1_认知错误','mean_steering_before','mean_steeringVelocity_before',
'sd_laneposition_before','turningCurve_before','laneCurve_before','sd_laneCurve_before','是否碰撞']  #全接管前的特征
features11 = ['mean_steering_before','mean_steeringVelocity_before',
'sd_laneposition_before','turningCurve_before','laneCurve_before','sd_laneCurve_before','是否碰撞']  #全接管前的纯驾驶特征


nf = len(features11)
selectdata = data[features11]

#全特征
#selectdata = data
#nf = len(data.columns)


#selectdata = selectdata.ix[selectdata['因子1_认知错误']!=0,:]#去掉因子为0的行


selectdata1 = selectdata.dropna()  #去掉所有带NA的行
#标准化
min_max_scaler = preprocessing.MinMaxScaler()
selectdata2 = pd.DataFrame(min_max_scaler.fit_transform(selectdata1))
selectdata2.columns = selectdata1.columns

#selectdata2 = selectdata.dropna()  #去掉所有带NA的行无标准化



x = selectdata2.drop('是否碰撞',1).values
y = selectdata2['是否碰撞'].values

DS = ClassificationDataSet(nf-1, 1, nb_classes=2)

for i in range(len(x)):
    DS.addSample(x[i], y[i])

trainTemp, testTemp = DS.splitWithProportion(0.9)

train = ClassificationDataSet(nf-1, 1, nb_classes=2)
for i in range(0, trainTemp.getLength()):
    train.addSample(trainTemp.getSample(i)[0], trainTemp.getSample(i)[1])

test = ClassificationDataSet(nf-1, 1, nb_classes=2)
for i in range(0, testTemp.getLength()):
    test.addSample(testTemp.getSample(i)[0], testTemp.getSample(i)[1])

train._convertToOneOfMany()
test._convertToOneOfMany()

nn = buildNetwork(train.indim, 1, train.outdim, hiddenclass=TanhLayer, outclass=SoftmaxLayer)
trainer = BackpropTrainer(nn, dataset=train, learningrate=0.1, momentum=0.1, verbose=True)
trainer.trainUntilConvergence(maxEpochs=50)

result = nn.activateOnDataset(test)

output = []

for i in range(len(result)):
    item=result[i]
    output.append((item.argmax(),test['class'][i][0]))
    
print (output)
print (100-percentError(trainer.testOnClassData(dataset=test), test['class']))


