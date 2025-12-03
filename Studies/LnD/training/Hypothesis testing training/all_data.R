all_data<-function(interval_val,xyz_flag){
  
  df<-feature_forall(interval_val,xyz_flag,1,0)
  
  for(i in 2:15){
    df<-rbind(df,feature_forall(interval_val,xyz_flag,i,0))
    
  }
  
  return(df)
  
}