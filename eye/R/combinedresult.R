setwd('F:\\GuoXiang\\˶ʿ��ҵ����\\DATA\\data\\4_reactiontime')
filenames <- list.files( pattern = ".csv")  #���ļ���������.csv�ļ�����ֵ��filenames
resultdata <- data.frame()   #�����հ����ݿ�
for ( i in filenames)
{
    b <- read.csv(i)
   
    resultdata<- rbind(resultdata,b)  #��ÿ�����Եļ�����ͳһ��һ�ű���
}

write.table(resultdata,"Reactiontime���ܱ�.csv",sep = ",",row.names = FALSE)
#���.csv