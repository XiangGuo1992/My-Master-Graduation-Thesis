import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.ticker as ticker

data = pd.read_csv('F:\\GuoXiang\\硕士毕业论文\\DATA\\result\\模型\\识别结果.csv',encoding='gbk')  #读取文件

#形成Y轴坐标数组
N = len(data)
ind = range(N)  # the evenly spaced plot indices
#ind1这里是为了把图撑大一点
ind1 = range(N+3)


fig = plt.figure(figsize=(11,5))
ax = fig.add_subplot(111)
#下行为了将图扩大一点，用白色线隐藏显示

plt.title("算法识别率")
plt.xlabel("LR")

ax.plot(ind, data['LR'], 'o-',label='LR')