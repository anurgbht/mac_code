diff_individual<-function(act1,act2,interval_val){
  act1<-1
  act2<-4
  interval_val<-1
  df<-feature_extraction(act1,act2,interval_val,1,0)
  
  for(i in 2:15){
    df<-rbind(df,feature_extraction(act1,act2,interval_val,i,0))
    
  }
  
  plot_ly(x=df$valence1,y=df$valence2,mode='markers',color=df$person_flag)
  
}