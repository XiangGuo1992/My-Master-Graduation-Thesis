setwd('F:\\GuoXiang\\˶ʿ��ҵ����\\DATA\\data\\4_ʱ��ڵ�')
filenames <- list.files( pattern = ".csv")  #���ļ���������.csv�ļ�����ֵ��filenames
resultdata <- data.frame()   #�����հ����ݿ�
for ( i in filenames)
{
    b <- read.csv(i)
    b[1,7]  <- i
    resultdata<- rbind(resultdata,b)  #��ÿ�����Եļ�����ͳһ��һ�ű���
}

write.table(resultdata,"ʱ��ڵ���ܱ�.csv",sep = ",",row.names = FALSE)
#���.csv