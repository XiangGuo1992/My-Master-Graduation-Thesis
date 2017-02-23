filenames <- list.files( pattern = ".csv") #将文件夹下所有.csv文件名赋值给filenames
for ( i in filenames)   #循环逐个处理.csv文件
{
    A <- read.csv(i)
    n <- nrow(A)        #计算文件的总行数
    n1 <- which(A[ ,1]==0)  #计算哪几列为0
    A[ ,1] <- A[ ,1]-A[length(n1)+1,1]   #修正时间
    A <- A[-n1, ]   #减去为0的前几列
    A1 <- subset(A,Type=='uv',select=c(Time,speedInKmPerHour,speedInMetresPerSecond,distanceTravelled,
                                   steering,steeringVelocity,turningCurvature,throttle
                                   ,brake,lightState,distanceAlongRoad,distanceToLeftBorder,distanceToRightBorder,offsetFromRoadCenter
                                   ,offsetFromLaneCenter,laneNumber,laneWidth,laneCurvature,drivingForwards)) 
    names(A1) <- c('fixedTime','speedInKmPerHour','speedInMetresPerSecond','distanceTravelled',
               'steering','steeringVelocity','turningCurvature','throttle'
               ,'brake','lightState','distanceAlongRoad','distanceToLeftBorder','distanceToRightBorder','offsetFromRoadCenter'
               ,'offsetFromLaneCenter','laneNumber','laneWidth','laneCurvature','drivingForwards')
    #将列名重命名为变量名
    write.csv(A1,paste("F:/GuoXiang/硕士毕业论文/DATA/data/2_filterdata/",i,sep = ''),row.names = FALSE)
}
