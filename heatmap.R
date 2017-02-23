<<<<<<< HEAD
setwd('F:\\GuoXiang\\硕士毕业论文\\DATA\\result\\模型')
rate <- read.csv('识别结果.csv')
rate <- rate[,-1]
trate <- t(rate)
colnames(trate) <- c('F0','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11')

library(pheatmap)
HM <- data.matrix(trate)
=======
setwd('F:\\GuoXiang\\硕士毕业论文\\DATA\\result\\模型')
rate <- read.csv('识别结果.csv')
rate <- rate[,-1]
trate <- t(rate)
colnames(trate) <- c('F0','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11')

library(pheatmap)
HM <- data.matrix(trate)
>>>>>>> 92a137b0eef95cdbc8e0c54bdf153c6c645aa234
pheatmap(HM,cluster_row = FALSE,cluster_col=FALSE)