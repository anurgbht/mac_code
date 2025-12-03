get_farthest <- function(cent_df){
  
  distance_metric<-numeric()
  
  nrow(cent_df)
  
  for(i in 1:nrow(cent_df)){
    for(j in i:nrow(cent_df)){
      if(i!=j){
      #print(c(i,j))
      (temp<-sqrt(sum((as.numeric(cent_df[i,1:5])-as.numeric(cent_df[j,1:5]))^2)))
      distance_metric<-rbind(distance_metric,(cbind(cent_df[i,6:8],cent_df[j,6:8],dist=temp)))
      #print('hello')
      #print(cbind(cent_df[i,6:8],cent_df[j,6:8]))
      }
    }
  }
  
  print(distance_metric)
 #return(distance_metric[distance_metric$dist==max(distance_metric$dist),]) 
  
  
}