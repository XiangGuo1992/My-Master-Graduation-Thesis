x <- read.csv('RT»ã×Ü±í.csv')
library(ggplot2)
ggplot(x)+geom_boxplot(aes(x=secondarytaskType, y=ToRT,fill=workloadLevel))+facet_wrap(~emergency)+theme_bw()+theme(legend.position=c(0.15,0.75),axis.title.x = element_text(size = 20),axis.text.x = element_text(size = 25),axis.text.y = element_text(size = 20),axis.title.y = element_text(size = 15)) +guides(fill = guide_legend(keywidth = 3, keyheight = 2.5))
        