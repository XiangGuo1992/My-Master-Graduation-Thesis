setwd('F:\\硕士毕业论文\\DATA\\physiological\\3_HR')
filenames <- list.files( pattern = ".csv")  #将文件夹下所有.csv文件名赋值给filenames
resultdata <- data.frame()   #创建空白数据框
for ( i in filenames)
{
    b <- read.csv(i)
   
    resultdata<- rbind(resultdata,b)  #将每个被试的计算结果统一到一张表格
}

write.table(resultdata,"生理数据汇总表.csv",sep = ",",row.names = FALSE)
#输出.csv