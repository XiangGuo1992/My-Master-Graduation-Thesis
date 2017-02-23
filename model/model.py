import os
import numpy as np
import pandas as pd
from pandas import read_csv 
os.chdir('F:\\硕士毕业论文\\DATA\\result\\模型')              #变更工作目录
                                          #列出所有文件

data = read_csv('collision模型.csv',encoding='gbk')  #读取文件
features1 = ['secondarytask','因子1_认知错误','sd_steering','sd_steeringVelocity','sd_laneposition',
'mean_steering_before','mean_steeringVelocity_before','sd_laneposition_before','turningCurve_before',
'laneCurve_before','sd_laneCurve_before','HR_sd_after','sac_times_after']  #完整的特征
features2 = ['secondarytask','因子1_认知错误','sd_steering','sd_steeringVelocity','sd_laneposition',
'mean_steering_before','mean_steeringVelocity_before','sd_laneposition_before','turningCurve_before',
'laneCurve_before','sd_laneCurve_before','HR_sd_after','sac_times_after']  #无眼动的特征
features3 = ['secondarytask','因子1_认知错误','mean_steering_before','mean_steeringVelocity_before',
'sd_laneposition_before','turningCurve_before','laneCurve_before','sd_laneCurve_before']  #全接管前的特征

selectdata = data[features3]
selectdata2 = selectdata.dropna()  #去掉所有带NA的行