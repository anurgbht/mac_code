feature_z <- function(act1,act2,interval_val,person_id){
  
  setwd('D:/Bhatt/2016-08/Hypothesis testing training')
  library('plotly')
  library('pracma')
  # analysis done only for a single person at present
  #act1<-1
  #act2<-4
  #interval_val<-1
  interval_val<-interval_val*52
  
  path<-paste('D:/Bhatt/2016-08/Hypothesis testing training/data/',as.character(person_id),'.csv',sep = '')
  temp1<-read.csv(path)
  
  colnames(temp1)<-c("index","x_acc","y_acc","z_acc","activity_flag")
  
  norm_acc <- sqrt((temp1$x_acc)^2 + (temp1$y_acc)^2 + (temp1$z_acc)^2)
  
  #int_set1<-norm_acc[temp1$activity_flag==act1]
  #int_set2<-norm_acc[temp1$activity_flag==act2]
  
  #offset<-mean(temp1$x_acc[temp1$activity_flag==1])
  
  #int_set1<-temp1$x_acc[temp1$activity_flag==act1]-offset
  #int_set2<-temp1$x_acc[temp1$activity_flag==act2]-offset
  
  #offset<-mean(temp1$y_acc[temp1$activity_flag==1])
  
  #int_set1<-temp1$y_acc[temp1$activity_flag==act1]-offset
  #int_set2<-temp1$y_acc[temp1$activity_flag==act2]-offset
  
  offset<-mean(temp1$z_acc[temp1$activity_flag==1])
  
  int_set1<-temp1$z_acc[temp1$activity_flag==act1]-offset
  int_set2<-temp1$z_acc[temp1$activity_flag==act2]-offset
  
  
  valence11 <- numeric()
  valence21 <- numeric()
  act_flag1<-numeric()
  valence12 <- numeric()
  valence22 <- numeric()
  act_flag2<-numeric()
  
  for( i in 1:floor(length(int_set1)/interval_val)){
    temp_ind<-(1+interval_val*(i-1)):((interval_val*2)+interval_val*(i-1))
    #print(temp_ind)
    tempset<-int_set1[temp_ind]
    
    valence11[i]<-sqrt(mean(tempset^2))
    #valence11[i]<-mean(tempset)
    #temp_val<-fft(tempset)
    #temp_val<- convert.fft(temp_val)
    #temp_val<-(temp_val$strength)/(length(temp_val$strength))
    #valence11[i]<-sum((temp_val)^2)
    
    #valence11[i]<-trapz(1:length(tempset),tempset)
    
    valence21[i]<-max(tempset)-min(tempset)
    act_flag1[i] <- act1
  }
  
  for( i in 1:floor(length(int_set2)/interval_val)){
    temp_ind<-(1+interval_val*(i-1)):((2*interval_val)+interval_val*(i-1))
    tempset<-int_set2[temp_ind]
    
    valence12[i]<-sqrt(mean(tempset^2))
    #valence12[i]<-mean(tempset)
    #temp_val<-fft(tempset)
    #temp_val<- convert.fft(temp_val)
    #temp_val<-(temp_val$strength)/(length(temp_val$strength))
    #valence12[i]<-sum((temp_val)^2)
    
    #valence12[i]<-trapz(1:length(tempset),tempset)
    
    valence22[i]<-max(tempset)-min(tempset)
    act_flag2[i] <- act2
  }
  
  
  df1 = data.frame(valence11,valence21,act_flag1)
  colnames(df1)<-c('valence1','valence2','act_flag')
  df2 = data.frame(valence12,valence22,act_flag2)
  colnames(df2)<-c('valence1','valence2','act_flag')
  df <- rbind(df1,df2)
  
  
  #save.image("valence_12.Rdata")
  
  #plot_ly(x=df$valence1,y=df$valence2,mode='markers',color=df$act_flag)
  #plot_ly(x=valence22,type='histogram')
  return(df)
}