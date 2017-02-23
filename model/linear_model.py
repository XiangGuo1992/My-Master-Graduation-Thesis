from sklearn import linear_model
from sklearn import metrics
from sklearn import cross_validation
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.chdir('F:\\硕士毕业论文\\DATA\\result\\模型')              #变更工作目录 
data = pd.read_csv('collision模型.csv',encoding='gbk')  #读取文件
features1 = ['secondarytask','因子1_认知错误','sd_steering','sd_steeringVelocity','sd_laneposition',
'mean_steering_before','mean_steeringVelocity_before','sd_laneposition_before','turningCurve_before',
'laneCurve_before','sd_laneCurve_before','HR_sd_after','sac_times_after','是否碰撞']  #完整的特征
features2 = ['secondarytask','因子1_认知错误','sd_steering','sd_steeringVelocity','sd_laneposition',
'mean_steering_before','mean_steeringVelocity_before','sd_laneposition_before','turningCurve_before',
'laneCurve_before','sd_laneCurve_before','HR_sd_after','是否碰撞']  #无眼动的特征
features3 = ['secondarytask','因子1_认知错误','mean_steering_before','mean_steeringVelocity_before',
'sd_laneposition_before','turningCurve_before','laneCurve_before','sd_laneCurve_before','是否碰撞']  #全接管前的特征
features4 = ['secondarytask','mean_steering_before','mean_steeringVelocity_before',
'sd_laneposition_before','turningCurve_before','laneCurve_before','sd_laneCurve_before','是否碰撞']  #全接管前的特征，无因子
features5 =  ['secondarytask','mean_steering_before','mean_steeringVelocity_before',
'sd_laneposition_before','turningCurve_before','sd_laneCurve_before','是否碰撞']  #全接管前的不相关特征，无因子

selectdata = data[features1]
#selectdata = selectdata.ix[selectdata['因子1_认知错误']!=0,:]#去掉因子为0的行
selectdata2 = selectdata.dropna()  #去掉所有带NA的行

x = selectdata2.drop('是否碰撞',1).values
y = selectdata2['是否碰撞'].values

X_train, X_test, y_train, y_test = cross_validation.train_test_split(x, y, test_size=0.1, random_state=0)


linear = linear_model.LinearRegression()

linear.fit(X_train, y_train)
linear.score(X_train, y_train)

print('Coefficient: n', linear.coef_)
print('Intercept: n', linear.intercept_)

predicted= linear.predict(X_test)

