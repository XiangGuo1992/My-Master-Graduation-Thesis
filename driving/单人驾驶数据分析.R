A <- read.csv(' 106.csv')
B <- data.frame()

if (length(levels(A[ ,19])) == 0)
{
    forward <- subset(A,drivingForwards == TRUE)
    backward <- subset(A,drivingForwards == FALSE) #区分前进与后退的路段
}
if (length(levels(A[ ,19])) == 2)
{
    forward <- subset(A,drivingForwards == 'True')
    backward <- subset(A,drivingForwards == 'False') #区分前进与后退的路段  
}

nf <- nrow(forward)    #统计向前的共有几行
nftime <- forward[,1]   #时间列
nfc <-NULL              #用于储存不同阶段的时间点
for (nfi in 1:(nf-1))    #如果下一行与上一行时间差超过10s，说明是不同的两段时间
{
    if ((nftime[nfi+1]-nftime[nfi])>100)
        nfc <- c(nfc,nfi)
}

#不同段的时间分别赋值给不同的变量

f1 <- forward[(nfc[1]+1):nfc[2], ]
f2 <- forward[(nfc[3]+1):nfc[4], ]
f3 <- forward[(nfc[4]+1):nf, ]



nb <- nrow(backward)    #统计向后的共有几行
nbtime <- backward[,1]   #时间列
nbc <-NULL              #用于储存不同阶段的时间点
for (nbi in 1:(nb-1))    #如果下一行与上一行时间差超过10s，说明是不同的两段时间
{
    if ((nbtime[nbi+1]-nbtime[nbi])>10)
        nbc <- c(nbc,nbi)
}

#不同段的时间分别赋值给不同的变量
b1 <- backward[(nbc[1]+1):nbc[2], ]
b2 <- backward[(nbc[2]+1):nb, ]

#第一段5km非紧急失效
nf1 <- nrow(f1)
f1checkpoint <- which(f1$distanceAlongRoad>5000)[1]     #找出提示点
f1peroid <- subset(f1,fixedTime>= (f1[f1checkpoint,1]) & fixedTime< (f1[f1checkpoint,1]+30))  #失效点前后30s

#计算何时切换
for (f1trans in 1:(nrow(f1peroid)-1))
{
    if ((f1peroid$lightState[f1trans] !=f1peroid$lightState[f1trans+1])  & (f1peroid$lightState[f1trans+1]=='' | f1peroid$lightState[f1trans+1]=='  BrakeLight'))  
        break
}
f1reactiontime <-  f1peroid$fixedTime[f1trans] - f1$fixedTime[f1checkpoint]  #从警报出现到切换反应时间

f1beforetrans <- subset(f1,fixedTime> (f1[f1checkpoint,1]-30) & fixedTime< f1[f1checkpoint,1])                   #切换前30s
f1intrans <- subset(f1,fixedTime>= (f1[f1checkpoint,1]) & fixedTime<= f1peroid$fixedTime[f1trans])                 #从request到切换
f1aftertrans <- subset(f1,fixedTime>f1peroid$fixedTime[f1trans] & fixedTime < (f1peroid$fixedTime[f1trans]+30))   #切换后30s

f1brakeRT <- f1aftertrans$fixedTime[which(f1aftertrans$brake > 0.05)[1]] - f1aftertrans$fixedTime[1]  #从切换至手动模式到开始刹车时间

write.csv(f1beforetrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','f1前',' 106.csv',sep = ""),row.names = FALSE)
write.csv(f1intrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','f1中',' 106.csv',sep = ""),row.names = FALSE)    
write.csv(f1aftertrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','f1后',' 106.csv',sep = ""),row.names = FALSE)       
B[1,1] <- f1reactiontime
B[1,2] <- f1brakeRT


#第2段6.49km紧急失效
nb1 <- nrow(b1)
b1checkpoint <- which(b1$distanceAlongRoad<6490)[1]     #找出提示点
b1peroid <- subset(b1,fixedTime>= (b1[b1checkpoint,1]) & fixedTime< (b1[b1checkpoint,1]+30))  #失效点前后30s

#计算何时切换
for (b1trans in 1:(nrow(b1peroid)-1))
{
    if (b1peroid$lightState[b1trans] !=b1peroid$lightState[b1trans+1] & (b1peroid$lightState[b1trans+1]=='  RightIndicator' | b1peroid$lightState[b1trans+1]=='  RightIndicator  BrakeLight'))   
        break
}
b1reactiontime <-  b1peroid$fixedTime[b1trans] - b1$fixedTime[b1checkpoint]  #从警报出现到切换反应时间

b1beforetrans <- subset(b1,fixedTime> (b1[b1checkpoint,1]-30) & fixedTime< b1[b1checkpoint,1])                   #切换前30s
b1intrans <- subset(b1,fixedTime>= (b1[b1checkpoint,1]) & fixedTime<= b1peroid$fixedTime[b1trans])                 #从request到切换
b1aftertrans <- subset(b1,fixedTime>b1peroid$fixedTime[b1trans] & fixedTime < (b1peroid$fixedTime[b1trans]+30))   #切换后30s

b1brakeRT <- b1aftertrans$fixedTime[which(b1aftertrans$brake > 0.05)[1]] - b1aftertrans$fixedTime[1]  #从切换至手动模式到开始刹车时间

write.csv(b1beforetrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','b1前',' 106.csv',sep = ""),row.names = FALSE)
write.csv(b1intrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','b1中',' 106.csv',sep = ""),row.names = FALSE)    
write.csv(b1aftertrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','b1后',' 106.csv',sep = ""),row.names = FALSE)       
B[1,3] <- b1reactiontime
B[1,4] <- b1brakeRT




#第三段1km非紧急失效
nf2 <- nrow(f2)
f2checkpoint <- which(f2$distanceAlongRoad>1000)[1]     #找出提示点
f2peroid <- subset(f2,fixedTime>= (f2[f2checkpoint,1]) & fixedTime< (f2[f2checkpoint,1]+30))  #失效点前后30s
#计算何时切换
for (f2trans in 1:(nrow(f2peroid)-1))
{
    if ((f2peroid$lightState[f2trans] !=f2peroid$lightState[f2trans+1])  & (f2peroid$lightState[f2trans+1]=='  RightIndicator' | f2peroid$lightState[f2trans+1]=='  RightIndicator  BrakeLight'))  
        break
}
f2reactiontime <-  f2peroid$fixedTime[f2trans] - f2$fixedTime[f2checkpoint]  #从警报出现到切换反应时间

f2beforetrans <- subset(f2,fixedTime> (f2[f2checkpoint,1]-30) & fixedTime< f2[f2checkpoint,1])                   #切换前30s
f2intrans <- subset(f2,fixedTime>= (f2[f2checkpoint,1]) & fixedTime<= f2peroid$fixedTime[f2trans])                 #从request到切换
f2aftertrans <- subset(f2,fixedTime>f2peroid$fixedTime[f2trans] & fixedTime < (f2peroid$fixedTime[f2trans]+30))   #切换后30s

f2brakeRT <- f2aftertrans$fixedTime[which(f2aftertrans$brake > 0.05)[1]] - f2aftertrans$fixedTime[1]  #从切换至手动模式到开始刹车时间
#从切换至手动模式到开始刹车时间

write.csv(f2beforetrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','f2前',' 106.csv',sep = ""),row.names = FALSE)
write.csv(f2intrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','f2中',' 106.csv',sep = ""),row.names = FALSE)    
write.csv(f2aftertrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','f2后',' 106.csv',sep = ""),row.names = FALSE)       
B[1,5] <- f2reactiontime
B[1,6] <- f2brakeRT





#第三段6km紧急失效

f2checkpoint2 <- which(f2$distanceAlongRoad>6000)[1]     #找出提示点
f2peroid2 <- subset(f2,fixedTime>= (f2[f2checkpoint2,1]) & fixedTime< (f2[f2checkpoint2,1]+30))  #失效点前后30s

#计算何时切换
for (f2trans2 in 1:(nrow(f2peroid2)-1))
{
    if (f2peroid2$lightState[f2trans2] !=f2peroid2$lightState[f2trans2+1] & (f2peroid2$lightState[f2trans2+1]=='  RightIndicator' | f2peroid2$lightState[f2trans2+1]=='  RightIndicator  BrakeLight'))   
        break
}
f2reactiontime2 <-  f2peroid2$fixedTime[f2trans2] - f2$fixedTime[f2checkpoint2]  #从警报出现到切换反应时间

f2beforetrans2 <- subset(f2,fixedTime> (f2[f2checkpoint2,1]-30) & fixedTime< f2[f2checkpoint2,1])                   #切换前30s
f2intrans2 <- subset(f2,fixedTime>= (f2[f2checkpoint2,1]) & fixedTime<= f2peroid2$fixedTime[f2trans2])                 #从request到切换
f2aftertrans2 <- subset(f2,fixedTime>f2peroid2$fixedTime[f2trans2] & fixedTime < (f2peroid2$fixedTime[f2trans2]+30))   #切换后30s

f2brakeRT2 <- f2aftertrans2$fixedTime[which(f2aftertrans2$brake > 0.05)[1]] - f2aftertrans2$fixedTime[1]  #从切换至手动模式到开始刹车时间
#从切换至手动模式到开始刹车时间

write.csv(f2beforetrans2,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','f2前2',' 106.csv',sep = ""),row.names = FALSE)
write.csv(f2intrans2,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','f2中2',' 106.csv',sep = ""),row.names = FALSE)    
write.csv(f2aftertrans2,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','f2后2',' 106.csv',sep = ""),row.names = FALSE)       
B[1,7] <- f2reactiontime2
B[1,8] <- f2brakeRT2



#第四段3.49km非紧急失效
nb2 <- nrow(b2)
b2checkpoint <- which(b2$distanceAlongRoad<3490)[1]     #找出提示点
b2peroid <- subset(b2,fixedTime>= (b2[b2checkpoint,1]) & fixedTime< (b2[b2checkpoint,1]+30))  #失效点前后30s

#计算何时切换
for (b2trans in 1:(nrow(b2peroid)-1))
{
    if (b2peroid$lightState[b2trans] !=b2peroid$lightState[b2trans+1] & (b2peroid$lightState[b2trans+1]=='  RightIndicator' | b2peroid$lightState[b2trans+1]=='  RightIndicator  BrakeLight'))   
        break
}
b2reactiontime <-  b2peroid$fixedTime[b2trans] - b2$fixedTime[b2checkpoint]  #从警报出现到切换反应时间

b2beforetrans <- subset(b2,fixedTime> (b2[b2checkpoint,1]-30) & fixedTime< b2[b2checkpoint,1])                   #切换前30s
b2intrans <- subset(b2,fixedTime>= (b2[b2checkpoint,1]) & fixedTime<= b2peroid$fixedTime[b2trans])                 #从request到切换
b2aftertrans <- subset(b2,fixedTime>b2peroid$fixedTime[b2trans] & fixedTime < (b2peroid$fixedTime[b2trans]+30))   #切换后30s

b2brakeRT <- b2aftertrans$fixedTime[which(b2aftertrans$brake > 0.05)[1]] - b2aftertrans$fixedTime[1]  #从切换至手动模式到开始刹车时间


write.csv(b2beforetrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','b2前',' 106.csv',sep = ""),row.names = FALSE)
write.csv(b2intrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','b2中',' 106.csv',sep = ""),row.names = FALSE)    
write.csv(b2aftertrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','b2后',' 106.csv',sep = ""),row.names = FALSE)       
B[1,9] <- b2reactiontime
B[1,10] <- b2brakeRT





#第五段2km紧急失效
f3checkpoint <- which(f3$distanceAlongRoad>2000)[1]     #找出提示点
f3peroid <- subset(f3,fixedTime>= (f3[f3checkpoint,1]) & fixedTime< (f3[f3checkpoint,1]+30))  #失效点前后30s

#计算何时切换
for (f3trans in 1:(nrow(f3peroid)-1))
{
    if (f3peroid$lightState[f3trans] !=f3peroid$lightState[f3trans+1] & (f3peroid$lightState[f3trans+1]=='  RightIndicator' | f3peroid$lightState[f3trans+1]=='  RightIndicator  BrakeLight'))   
        break
}
f3reactiontime <-  f3peroid$fixedTime[f3trans] - f3$fixedTime[f3checkpoint]  #从警报出现到切换反应时间

f3beforetrans <- subset(f3,fixedTime> (f3[f3checkpoint,1]-30) & fixedTime< f3[f3checkpoint,1])                   #切换前30s
f3intrans <- subset(f3,fixedTime>= (f3[f3checkpoint,1]) & fixedTime<= f3peroid$fixedTime[f3trans])                 #从request到切换
f3aftertrans <- subset(f3,fixedTime>f3peroid$fixedTime[f3trans] & fixedTime < (f3peroid$fixedTime[f3trans]+30))   #切换后30s

f3brakeRT <- f3aftertrans$fixedTime[which(f3aftertrans$brake > 0.05)[1]] - f3aftertrans$fixedTime[1]  #从切换至手动模式到开始刹车时间
#从切换至手动模式到开始刹车时间

write.csv(f3beforetrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','f3前',' 106.csv',sep = ""),row.names = FALSE)
write.csv(f3intrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','f3中',' 106.csv',sep = ""),row.names = FALSE)    
write.csv(f3aftertrans,paste('F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/3_sectiondata/','f3后',' 106.csv',sep = ""),row.names = FALSE)       
B[1,11] <- f3reactiontime
B[1,12] <- f3brakeRT

write.csv(B,paste("F:/GuoXiang/毕业设计/吴恩泽/实验数据/driving data/4_reactiontime/",' 106.csv'),row.names = FALSE)