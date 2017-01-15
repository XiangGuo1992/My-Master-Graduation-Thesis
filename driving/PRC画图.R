x <- read.csv('PRC»ã×Ü.csv')
library(ggplot2)
ggplot(x)+geom_boxplot(aes(x=secondarytaskType, y=after_PRC,fill=secondarytaskLevel))+theme_bw()+facet_wrap(~emergency)+theme(legend.position=c(0.5,0.2),axis.title.x = element_text(size = 15),axis.text.x = element_text(size = 15),axis.title.y = element_text(size = 12))
ggplot(x)+geom_boxplot(aes(x=secondarytaskType, y=before_PRC,fill=secondarytaskLevel))+theme_bw()+facet_wrap(~emergency)+theme(legend.position=c(0.45,0.25),axis.title.x = element_text(size = 20),axis.text.x = element_text(size = 20),axis.text.y = element_text(size = 20),axis.title.y = element_text(size = 20))+guides(fill = guide_legend(keywidth = 3, keyheight = 2))
