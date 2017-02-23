from sklearn.naive_bayes import GaussianNB
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import cross_validation
from sklearn.cross_validation import LeaveOneOut
from sklearn import preprocessing

os.chdir('F:\\硕士毕业论文\\DATA\\result\\模型')              #变更工作目录 
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


selectdata = data[features11]
#selectdata = data
selectdata = selectdata.ix[selectdata['因子1_认知错误']!=0,:]#去掉因子为0的行

selectdata1 = selectdata.dropna()  #去掉所有带NA的行
#标准化
min_max_scaler = preprocessing.MinMaxScaler()
selectdata2 = pd.DataFrame(min_max_scaler.fit_transform(selectdata1))
selectdata2.columns = selectdata1.columns

#selectdata2 = selectdata.dropna()  #去掉所有带NA的行无标准化


x = selectdata2.drop('是否碰撞',1).values
y = selectdata2['是否碰撞'].values
result = []

#LOOCV验证
loo= LeaveOneOut(len(y)) 
for train, test in loo: 
	clf = GaussianNB()
	clf.fit(x[train], y[train])
	print(clf.score(x[test], y[test]))
	result.append(clf.score(x[test], y[test]))
print(np.mean(result))



