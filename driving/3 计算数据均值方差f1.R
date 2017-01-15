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
    R <- rbind(R,r)
       
}
colnames(R) <- c('subject','mean_speed(km/h)','sd_speed(km/h)','mean_steering','sd_steering','mean_steeringVelocity','sd_steeringVelocity',
                 'max_brake', 'mean_laneposition','sd_laneposition')
write.csv(R,"f1接管后汇总表.csv",row.names = FALSE)