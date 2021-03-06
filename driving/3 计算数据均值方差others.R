setwd('F:/硕士毕业论文/DATA/data/3_sectiondata/接管前')
filenames <- list.files( pattern = ".csv") #将文件夹下所有.csv文件名赋值给filenames
r <- data.frame()   #创建空白数据框
R <- data.frame()
for ( i in filenames)   #循环逐个处理.csv文件
{
    a <- read.csv(i)   
    r[1,1] <- i
    r[1,2] <- mean(a$speedInKmPerHour)
    r[1,3] <- sd(a$speedInKmPerHour)
    r[1,4] <- mean(a$steering)
    r[1,5] <- sd(a$steering)
    r[1,6] <- mean(a$steeringVelocity)
    r[1,7] <- sd(a$steeringVelocity)
    r[1,8] <- max(a$brake)
    r[1,9] <- mean(a$offsetFromLaneCenter)
    r[1,10] <- sd(a$offsetFromLaneCenter)
    r[1,11] <- mean(a$turningCurvature)
    r[1,12] <- sd(a$turningCurvature)
    r[1,13] <- mean(a$laneCurvature)
    r[1,14] <- sd(a$laneCurvature)
    R <- rbind(R,r)
    
}
colnames(R) <- c('subject','mean_speed(km/h)','sd_speed(km/h)','mean_steering','sd_steering','mean_steeringVelocity','sd_steeringVelocity',
                 'max_brake', 'mean_laneposition','sd_laneposition','turningCurve','sd_turningCurve','laneCurve','sd_laneCurve')
write.csv(R,"接管前汇总表.csv",row.names = FALSE)

