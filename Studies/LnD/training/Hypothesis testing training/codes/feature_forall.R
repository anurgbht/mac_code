feature_forall <- function(interval_val,xyz_flag,person_id,plot_flag){
  
  setwd('D:/Bhatt/2016-08/Hypothesis testing training')
  library('plotly')
  library('pracma')
  
  interval_val<-interval_val*52
  
  path<-paste('D:/Bhatt/2016-08/Hypothesis testing training/data/',as.character(person_id),'.csv',sep = '')
  temp1<-read.csv(path)
  colnames(temp1)<-c("index","x_acc","y_acc","z_acc","activity_flag")
  
  norm_acc <- sqrt((temp1$x_acc)^2 + (temp1$y_acc)^2 + (temp1$z_acc)^2)
  
  if(xyz_flag=='x'){
  int_set1<-temp1$x_acc[temp1$activity_flag==1]
  int_set2<-temp1$x_acc[temp1$activity_flag==2]
  int_set3<-temp1$x_acc[temp1$activity_flag==3]
  int_set4<-temp1$x_acc[temp1$activity_flag==4]
  int_set5<-temp1$x_acc[temp1$activity_flag==5]
  int_set6<-temp1$x_acc[temp1$activity_flag==6]
  int_set7<-temp1$x_acc[temp1$activity_flag==7]
  }else if(xyz_flag=='y'){
    int_set1<-temp1$y_acc[temp1$activity_flag==1]
    int_set2<-temp1$y_acc[temp1$activity_flag==2]
    int_set3<-temp1$y_acc[temp1$activity_flag==3]
    int_set4<-temp1$y_acc[temp1$activity_flag==4]
    int_set5<-temp1$y_acc[temp1$activity_flag==5]
    int_set6<-temp1$y_acc[temp1$activity_flag==6]
    int_set7<-temp1$y_acc[temp1$activity_flag==7]
  }else if(xyz_flag=='z'){
    int_set1<-temp1$z_acc[temp1$activity_flag==1]
    int_set2<-temp1$z_acc[temp1$activity_flag==2]
    int_set3<-temp1$z_acc[temp1$activity_flag==3]
    int_set4<-temp1$z_acc[temp1$activity_flag==4]
    int_set5<-temp1$z_acc[temp1$activity_flag==5]
    int_set6<-temp1$z_acc[temp1$activity_flag==6]
    int_set7<-temp1$z_acc[temp1$activity_flag==7]
  }
  valence11 <- numeric()
  valence21 <- numeric()
  act_flag1<-numeric()
  
  valence12 <- numeric()
  valence22 <- numeric()
  act_flag2<-numeric()
  
  valence13 <- numeric()
  valence23 <- numeric()
  act_flag3<-numeric()
  
  valence14 <- numeric()
  valence24 <- numeric()
  act_flag4<-numeric()
  
  valence15 <- numeric()
  valence25 <- numeric()
  act_flag5<-numeric()
  
  valence16 <- numeric()
  valence26 <- numeric()
  act_flag6<-numeric()
  
  valence17 <- numeric()
  valence27 <- numeric()
  act_flag7<-numeric()
  
  valence31<-numeric()
  valence32<-numeric()
  valence33<-numeric()
  valence34<-numeric()
  valence35<-numeric()
  valence36<-numeric()
  valence37<-numeric()
  
  valence41<-numeric()
  valence42<-numeric()
  valence43<-numeric()
  valence44<-numeric()
  valence45<-numeric()
  valence46<-numeric()
  valence47<-numeric()
  
  valence51<-numeric()
  valence52<-numeric()
  valence53<-numeric()
  valence54<-numeric()
  valence55<-numeric()
  valence56<-numeric()
  valence57<-numeric()
  
  
  for( i in 1:floor(length(int_set1)/interval_val)){
    temp_ind<-(1+interval_val*(i-1)):((interval_val*2)+interval_val*(i-1))
    #print(temp_ind)
    tempset<-int_set1[temp_ind]
    
    valence31[i]<-sqrt(mean(tempset^2))
    valence41[i]<-mean(tempset)
    temp_val<-fft(tempset)
    temp_val<- convert.fft(temp_val)
    temp_val<-(temp_val$strength)/(length(temp_val$strength))
    valence51[i]<-sum((temp_val)^2)
    valence11[i]<-trapz(1:length(tempset),tempset)
    
    valence21[i]<-max(tempset)-min(tempset)
    act_flag1[i] <- 1
  }
  
  for( i in 1:floor(length(int_set2)/interval_val)){
    temp_ind<-(1+interval_val*(i-1)):((2*interval_val)+interval_val*(i-1))
    tempset<-int_set2[temp_ind]
    
    valence32[i]<-sqrt(mean(tempset^2))
    valence42[i]<-mean(tempset)
    temp_val<-fft(tempset)
    temp_val<- convert.fft(temp_val)
    temp_val<-(temp_val$strength)/(length(temp_val$strength))
    valence52[i]<-sum((temp_val)^2)
    valence12[i]<-trapz(1:length(tempset),tempset)
    
    valence22[i]<-max(tempset)-min(tempset)
    act_flag2[i] <- 2
  }
  
  for( i in 1:floor(length(int_set3)/interval_val)){
    temp_ind<-(1+interval_val*(i-1)):((2*interval_val)+interval_val*(i-1))
    tempset<-int_set3[temp_ind]
    
    valence33[i]<-sqrt(mean(tempset^2))
    valence43[i]<-mean(tempset)
    temp_val<-fft(tempset)
    temp_val<- convert.fft(temp_val)
    temp_val<-(temp_val$strength)/(length(temp_val$strength))
    valence53[i]<-sum((temp_val)^2)
    valence13[i]<-trapz(1:length(tempset),tempset)
    valence23[i]<-max(tempset)-min(tempset)
    act_flag3[i] <- 3
  }
  
  for( i in 1:floor(length(int_set4)/interval_val)){
    temp_ind<-(1+interval_val*(i-1)):((2*interval_val)+interval_val*(i-1))
    tempset<-int_set4[temp_ind]
    
    valence34[i]<-sqrt(mean(tempset^2))
    valence44[i]<-mean(tempset)
    temp_val<-fft(tempset)
    temp_val<- convert.fft(temp_val)
    temp_val<-(temp_val$strength)/(length(temp_val$strength))
    valence54[i]<-sum((temp_val)^2)
    valence14[i]<-trapz(1:length(tempset),tempset)
    valence24[i]<-max(tempset)-min(tempset)
    act_flag4[i] <- 4
  }
  
  for( i in 1:floor(length(int_set5)/interval_val)){
    temp_ind<-(1+interval_val*(i-1)):((2*interval_val)+interval_val*(i-1))
    tempset<-int_set5[temp_ind]
    
    valence35[i]<-sqrt(mean(tempset^2))
    valence45[i]<-mean(tempset)
    temp_val<-fft(tempset)
    temp_val<- convert.fft(temp_val)
    temp_val<-(temp_val$strength)/(length(temp_val$strength))
    valence55[i]<-sum((temp_val)^2)
    valence15[i]<-trapz(1:length(tempset),tempset)
    valence25[i]<-max(tempset)-min(tempset)
    act_flag5[i] <- 5
  }
  
  for( i in 1:floor(length(int_set6)/interval_val)){
    temp_ind<-(1+interval_val*(i-1)):((2*interval_val)+interval_val*(i-1))
    tempset<-int_set6[temp_ind]
    
    valence36[i]<-sqrt(mean(tempset^2))
    valence46[i]<-mean(tempset)
    temp_val<-fft(tempset)
    temp_val<- convert.fft(temp_val)
    temp_val<-(temp_val$strength)/(length(temp_val$strength))
    valence56[i]<-sum((temp_val)^2)
    valence16[i]<-trapz(1:length(tempset),tempset)
    valence26[i]<-max(tempset)-min(tempset)
    act_flag6[i] <- 6
  }
  
  for( i in 1:floor(length(int_set7)/interval_val)){
    temp_ind<-(1+interval_val*(i-1)):((2*interval_val)+interval_val*(i-1))
    tempset<-int_set7[temp_ind]
    
    valence37[i]<-sqrt(mean(tempset^2))
    valence47[i]<-mean(tempset)
    temp_val<-fft(tempset)
    temp_val<- convert.fft(temp_val)
    temp_val<-(temp_val$strength)/(length(temp_val$strength))
    valence57[i]<-sum((temp_val)^2)
    valence17[i]<-trapz(1:length(tempset),tempset)
    valence27[i]<-max(tempset)-min(tempset)
    act_flag7[i] <- 7
  }
  
  
  df1 = data.frame(valence11,valence21,valence31,valence41,valence51,act_flag1)
  colnames(df1)<-c('valence1','valence2','valence3','valence4','valence5','act_flag')
  df2 = data.frame(valence12,valence22,valence32,valence42,valence52,act_flag2)
  colnames(df2)<-c('valence1','valence2','valence3','valence4','valence5','act_flag')
  df3 = data.frame(valence13,valence23,valence33,valence43,valence53,act_flag3)
  colnames(df3)<-c('valence1','valence2','valence3','valence4','valence5','act_flag')
  df4 = data.frame(valence14,valence24,valence34,valence44,valence54,act_flag4)
  colnames(df4)<-c('valence1','valence2','valence3','valence4','valence5','act_flag')
  df5 = data.frame(valence15,valence25,valence35,valence45,valence55,act_flag5)
  colnames(df5)<-c('valence1','valence2','valence3','valence4','valence5','act_flag')
  df6 = data.frame(valence16,valence26,valence36,valence46,valence56,act_flag6)
  colnames(df6)<-c('valence1','valence2','valence3','valence4','valence5','act_flag')
  df7 = data.frame(valence17,valence27,valence37,valence47,valence57,act_flag7)
  colnames(df7)<-c('valence1','valence2','valence3','valence4','valence5','act_flag')
  
  
  df <- rbind(df1,df2,df3,df4,df5,df6,df7)
  df['person_flag']<-person_id
  
  #save.image("valence_12.Rdata")
  if (plot_flag){
    plot_ly(x=df$valence1,y=df$valence2,mode='markers',color=df$act_flag)
  } else{
    return(df)
  }
  
}