setwd('F:\\GuoXiang\\˶ʿ��ҵ����\\DATA\\result\\ģ��')
library(ggplot2)
rate <- read.csv('ʶ����.csv')
ggplot(rate,aes(x=FeaturesSet,y=KNN,group=1))  +ggtitle ("KNN�㷨ʶ���ʽ��") +geom_line(size=1.5,
                                    colour = "deepskyblue4") + geom_point(size=4,colour = "deepskyblue4" ) + scale_x_continuous( breaks=0:11)+ scale_y_continuous(limits = c(0.45, 1),breaks=seq(0.5, 1, 
by = 0.1)) + theme_bw() +ylab('ʶ����') +xlab('��������') +theme(plot.title = element_text(size=25,face = "bold",hjust = 0.5), 
                 axis.title.x = element_text(size = 23,face = "bold"), 
                 axis.text.x = element_text(size = 20,face = "bold"), 
                 axis.title.y = element_text(size = 23,face = "bold"), 
                 axis.text.y = element_text(size = 20,face = "bold")    )   
