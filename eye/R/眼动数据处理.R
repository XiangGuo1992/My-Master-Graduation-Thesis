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

filenames <- list.files(pattern = '.csv')    
for (i in 1:length(filenames))
{
    A <- read.csv(filenames[i])
    a <- subset(A,GazeDirectionQ > 0.5, select =c(time,GazeHeading,GazePitch))
    #GazeDirection.x,GazeDirection.y,GazeDirection.z,FilteredLeftGazeHeading,FilteredLeftGazePitch
    B <- data.frame()
    
    #时间修正
    a$time <- a$time - timedelay[i,2]
    #单位转化
    a$GazeHeading[a$GazeHeading >0] <- 180 - a$GazeHeading[a$GazeHeading >0]*180/pi
    a$GazeHeading[a$GazeHeading <0] <- -a$GazeHeading[a$GazeHeading <0]*180/pi-180    
    a$GazePitch <- a$GazePitch*180/pi
    
    
    f1before <- subset(a,time > (timepoint[i,2]-90) & time < timepoint[i,2] )
    f1after <- subset(a,time > timepoint[i,2] & time < (timepoint[i,2]+30) )
    
    B[1,1] <- filenames[i]
    B[1,2] <- 0
    B[1,3] <- 0
    B[1,4] <- calDTC(f1before$GazeHeading,f1before$GazePitch,findRC(f1before$GazeHeading),findRC(f1before$GazePitch))
    B[1,5] <- calDTC(f1after$GazeHeading,f1after$GazePitch,findRC(f1after$GazeHeading),findRC(f1after$GazePitch))
    
    
    b1before <- subset(a,time > (timepoint[i,3]-90) & time < timepoint[i,3]  )
    b1after <- subset(a,time > timepoint[i,3] & time < (timepoint[i,3]+30) )
    
    B[2,1] <- filenames[i]
    B[2,2] <- 0
    B[2,3] <- 1
    B[2,4] <- calDTC(b1before$GazeHeading,b1before$GazePitch,findRC(b1before$GazeHeading),findRC(b1before$GazePitch))    
    B[2,5] <- calDTC(b1after$GazeHeading,b1after$GazePitch,findRC(b1after$GazeHeading),findRC(b1after$GazePitch))    
    
    
    f2before <- subset(a,time > (timepoint[i,4]-90) & time < timepoint[i,4]  )
    f2after <- subset(a,time > timepoint[i,4] & time < (timepoint[i,4]+30) )
    
    B[3,1] <- filenames[i]
    B[3,2] <- 1
    B[3,3] <- 0
    B[3,4] <- calDTC(f2before$GazeHeading,f2before$GazePitch,findRC(f2before$GazeHeading),findRC(f2before$GazePitch))
    B[3,5] <- calDTC(f2after$GazeHeading,f2after$GazePitch,findRC(f2after$GazeHeading),findRC(f2after$GazePitch))

    
    
    f2before2 <- subset(a,time > (timepoint[i,5]-90) & time < timepoint[i,5]  )
    f2after2 <- subset(a,time > timepoint[i,5] & time < (timepoint[i,5]+30) )   

    B[4,1] <- filenames[i]
    B[4,2] <- 1
    B[4,3] <- 1
    B[4,4] <- calDTC(f2before2$GazeHeading,f2before2$GazePitch,findRC(f2before2$GazeHeading),findRC(f2before2$GazePitch))
    B[4,5] <- calDTC(f2after2$GazeHeading,f2after2$GazePitch,findRC(f2after2$GazeHeading),findRC(f2after2$GazePitch))    
    
    
    
    b2before <- subset(a,time > (timepoint[i,6]-90) & time < timepoint[i,6]  )
    b2after <- subset(a,time > timepoint[i,6] & time < (timepoint[i,6]+30) )
    
    B[5,1] <- filenames[i]
    B[5,2] <- 2
    B[5,3] <- 0
    B[5,4] <- calDTC(b2before$GazeHeading,b2before$GazePitch,findRC(b2before$GazeHeading),findRC(b2before$GazePitch))
    B[5,5] <- calDTC(b2after$GazeHeading,b2after$GazePitch,findRC(b2after$GazeHeading),findRC(b2after$GazePitch))
    
    
    
    f3before <- subset(a,time > (timepoint[i,7]-90) & time < timepoint[i,7]  )
    f3after <- subset(a,time > timepoint[i,7] & time < (timepoint[i,7]+30) )
    
    B[6,1] <- filenames[i]
    B[6,2] <- 2
    B[6,3] <- 1
    B[6,4] <- calDTC(f3before$GazeHeading,f3before$GazePitch,findRC(f3before$GazeHeading),findRC(f3before$GazePitch))
    B[6,5] <- calDTC(f3after$GazeHeading,f3after$GazePitch,findRC(f3after$GazeHeading),findRC(f3after$GazePitch))
    
    
    colnames(B) <- c('subject','secondarytask','emergency','before_PRC','after_PRC') 
    write.csv(B,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/eye data/PRC/',filenames[i],sep = ''),row.names = F)
    
}