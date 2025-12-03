hist_sub <- function(act_id,person_id,valence_id,axis_id){
  
  library('plotly')
  load("D:/Bhatt/2016-08/Hypothesis testing training/assdata.RData")
  
  temp<-df[,valence_id]
  temp<-temp[(df$act_flag == act_id)&(df$person_flag == person_id)&(df$axis_flag == axis_id)]
  
  plot_ly(x=temp,type='histogram')
  
}