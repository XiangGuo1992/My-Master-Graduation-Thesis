setwd('F:\\GuoXiang\\硕士毕业论文\\DATA\\result\\模型')
library(ggplot2)
rate <- read.csv('识别结果.csv')
ggplot(rate,aes(x=FeaturesSet,y=KNN,group=1))  +ggtitle ("KNN算法识别率结果") +geom_line(size=1.5,
                                    colour = "deepskyblue4") + geom_point(size=4,colour = "deepskyblue4" ) + scale_x_continuous( breaks=0:11)+ scale_y_continuous(limits = c(0.45, 1),breaks=seq(0.5, 1, 
by = 0.1)) + theme_bw() +ylab('识别率') +xlab('特征集合') +theme(plot.title = element_text(size=25,face = "bold",hjust = 0.5), 
                 axis.title.x = element_text(size = 23,face = "bold"), 
                 axis.text.x = element_text(size = 20,face = "bold"), 
                 axis.title.y = element_text(size = 23,face = "bold"), 
                 axis.text.y = element_text(size = 20,face = "bold")    )   

