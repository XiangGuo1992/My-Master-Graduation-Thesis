timepoint <- read.csv('F:/GuoXiang/毕业设计/吴恩泽/实验数据/eye data/时间节点汇总表.csv')
timedelay <- read.csv('F:/GuoXiang/毕业设计/吴恩泽/实验数据/eye data/timedelay.csv')

#自编查找道路中心函数
findRC <- function(x)
{
    bins <- seq(min(x),max(x),by=1)
    n <- data.frame()
    for (i in 1:(length(bins)-1))
    {
        n[i,1] <-  (bins[i] + bins[i+1])/2
        n[i,2] <-  length(which(x > bins[i] & x < bins[i+1]))
    }
    return (n[which.max(n[ ,2]),1])
    
}


#自编计算距离及百分比函数
calDTC <- function(head,pitch,x,y)
{
    j <- 0
    n <- length(head)
    for (i in 1:n)
    {
        if (sqrt((head[i]-x)^2+(pitch[i]-y)^2) < 16)
        {j <- j+1}
    }
    return (j/n)
}

califC <- function(i,j,k,l)
{
    a <- c()
    for (x in 1:length(i))
    {
        if (sqrt((i[x]-k)^2+(j[x]-l)^2) < 16)        a[x] <- 'RoadCenter'
        else a[x] <-'RoadEdge'
    }
    return (a)
    
}


library(ggplot2)

    A <- read.csv('104.csv')
    a <- subset(A,GazeDirectionQ > 0.5, select =c(time,GazeHeading,GazePitch))
    #GazeDirection.x,GazeDirection.y,GazeDirection.z,FilteredLeftGazeHeading,FilteredLeftGazePitch
    B <- data.frame()
    
    #时间修正
    a$time <- a$time - timedelay[4,2]
    #单位转化
    a$GazeHeading[a$GazeHeading >0] <- 180 - a$GazeHeading[a$GazeHeading >0]*180/pi
    a$GazeHeading[a$GazeHeading <0] <- -a$GazeHeading[a$GazeHeading <0]*180/pi-180    
    a$GazePitch <- a$GazePitch*180/pi
    
    
    f1before <- subset(a,time > (timepoint[4,2]-90) & time < timepoint[4,2] )
    f1after <- subset(a,time > timepoint[4,2] & time < (timepoint[4,2]+30) )
    
    HC <- findRC(f1before$GazeHeading)
    PC <- findRC(f1before$GazePitch)
    
    f1before[,4] <- califC(f1before[ ,2],f1before[ ,3],HC,PC)
    colnames(f1before)[4] <- 'RoadGaze'
    
    p <- ggplot(f1before,aes(x=GazeHeading, y=GazePitch, colour=factor(RoadGaze)))
    p + geom_point()+ggtitle('Gaze Distribution Before Take-over')+scale_colour_manual(values=rainbow(3))+theme_bw()+theme(legend.title = element_text(size=20),legend.text = element_text(size = 20, face = "bold"),plot.title = element_text(size=22,face = "bold"),legend.position=c(0.8,0.2),axis.title.x = element_text(size = 25),axis.text.x = element_text(size = 25),axis.title.y = element_text(size = 25),axis.text.y = element_text(size = 25))
    
    HC <- findRC(f1after$GazeHeading)
    PC <- findRC(f1after$GazePitch)
    
    f1after[,4] <- califC(f1after[ ,2],f1after[ ,3],HC,PC)
    colnames(f1after)[4] <- 'RoadGaze'
    
    p <- ggplot(f1after,aes(x=GazeHeading, y=GazePitch, colour=factor(RoadGaze)))
    p + geom_point()+ggtitle('Gaze Distribution After Take-over')+scale_colour_manual(values=rainbow(3))+theme_bw()+theme(legend.title = element_text(size=20),legend.text = element_text(size = 20, face = "bold"),plot.title = element_text(size=22,face = "bold"),legend.position=c(0.8,0.2),axis.title.x = element_text(size = 25),axis.text.x = element_text(size = 25),axis.title.y = element_text(size = 25),axis.text.y = element_text(size = 25))
    
    
    
    
    b1before <- subset(a,time > (timepoint[4,3]-90) & time < timepoint[4,3]  )
    b1after <- subset(a,time > timepoint[4,3] & time < (timepoint[4,3]+30) )
    
    HC <- findRC(b1before$GazeHeading)
    PC <- findRC(b1before$GazePitch)
    
    b1before[,4] <- califC(b1before[ ,2],b1before[ ,3],HC,PC)
    names(b1before) <- c('time','GazeHeading','GazePitch','gaze')
    
    p <- ggplot(b1before,aes(x=GazeHeading, y=GazePitch, colour=factor(gaze)))
    p + geom_point()+scale_x_continuous(limits=c(-60,60))+scale_y_continuous(limits=c(-60,0))+theme_bw()+ggtitle ("Gaze distribution before take-over" )
   
    
    HC <- findRC(b1after$GazeHeading)
    PC <- findRC(b1after$GazePitch)
    
    b1after[,4] <- califC(b1after[ ,2],b1after[ ,3],HC,PC)
    names(b1after) <- c('time','GazeHeading','GazePitch','gaze')
    
    p <- ggplot(b1after,aes(x=GazeHeading, y=GazePitch, colour=factor(gaze)))
    p + geom_point()+scale_x_continuous(limits=c(-60,60))+scale_y_continuous(limits=c(-60,0))+theme_bw()+ggtitle ("Gaze distribution after take-over" )
    
    
    

    
    
    
    f2before <- subset(a,time > (timepoint[4,4]-90) & time < timepoint[4,4]  )
    f2after <- subset(a,time > timepoint[4,4] & time < (timepoint[4,4]+30) )
    
    HC <- findRC(f2before$GazeHeading)
    PC <- findRC(f2before$GazePitch)
    
    f2before[,4] <- califC(f2before[ ,2],f2before[ ,3],HC,PC)
    
    p <- ggplot(f2before,aes(x=GazeHeading, y=GazePitch, colour=factor(V4)))
    p + geom_point()
    
    HC <- findRC(f2after$GazeHeading)
    PC <- findRC(f2after$GazePitch)
    
    f2after[,4] <- califC(f2after[ ,2],f2after[ ,3],HC,PC)
    
    p <- ggplot(f2after,aes(x=GazeHeading, y=GazePitch, colour=factor(V4)))
    p + geom_point()
    
    
    
    
    
    
    f2before2 <- subset(a,time > (timepoint[4,5]-90) & time < timepoint[4,5]  )
    f2after2 <- subset(a,time > timepoint[4,5] & time < (timepoint[4,5]+30) )   
    
    HC <- findRC(f2before2$GazeHeading)
    PC <- findRC(f2before2$GazePitch)
    
    f2before2[,4] <- califC(f2before2[ ,2],f2before2[ ,3],HC,PC)
    
    p <- ggplot(f2before2,aes(x=GazeHeading, y=GazePitch, colour=factor(V4)))
    p + geom_point()
    
    HC <- findRC(f2after2$GazeHeading)
    PC <- findRC(f2after2$GazePitch)
    
    f2after2[,4] <- califC(f2after2[ ,2],f2after2[ ,3],HC,PC)
    
    p <- ggplot(f2after2,aes(x=GazeHeading, y=GazePitch, colour=factor(V4)))
    p + geom_point()
    
    
    
    
    
    b2before <- subset(a,time > (timepoint[4,6]-90) & time < timepoint[4,6]  )
    b2after <- subset(a,time > timepoint[4,6] & time < (timepoint[4,6]+30) )
    
    HC <- findRC(b2before$GazeHeading)
    PC <- findRC(b2before$GazePitch)
    
    b2before[,4] <- califC(b2before[ ,2],b2before[ ,3],HC,PC)
    
    p <- ggplot(b2before,aes(x=GazeHeading, y=GazePitch, colour=factor(V4)))
    p + geom_point()
    
    HC <- findRC(b2after$GazeHeading)
    PC <- findRC(b2after$GazePitch)
    
    b2after[,4] <- califC(b2after[ ,2],b2after[ ,3],HC,PC)
    
    p <- ggplot(b2after,aes(x=GazeHeading, y=GazePitch, colour=factor(V4)))
    p + geom_point()
    
    
    
    f3before <- subset(a,time > (timepoint[4,7]-90) & time < timepoint[4,7]  )
    f3after <- subset(a,time > timepoint[4,7] & time < (timepoint[4,7]+30) )
    
    HC <- findRC(f3before$GazeHeading)
    PC <- findRC(f3before$GazePitch)
    
    f3before[,4] <- califC(f3before[ ,2],f3before[ ,3],HC,PC)
    
    p <- ggplot(f3before,aes(x=GazeHeading, y=GazePitch, colour=factor(V4)))
    p + geom_point()
    
    HC <- findRC(f3after$GazeHeading)
    PC <- findRC(f3after$GazePitch)
    
    f3after[,4] <- califC(f3after[ ,2],f3after[ ,3],HC,PC)
    
    p <- ggplot(f3after,aes(x=GazeHeading, y=GazePitch, colour=factor(V4)))
    p + geom_point()
    
    
    colnames(B) <- c('subject','secondarytask','emergency','before_PRC','after_PRC') 
    write.csv(B,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/eye data/PRC/',filenames[i],sep = ''),row.names = F)
    
