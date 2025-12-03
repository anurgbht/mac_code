dis_centroid <- function(){
  
  load("D:/Bhatt/2016-08/Hypothesis testing training/assdata.RData")
  
  v1<-df$valence1
  v2<-df$valence2
  v3<-df$valence3
  v4<-df$valence4
  v5<-df$valence5
  
  # centroid_df<-data.frame(av1=numeric(),av2=numeric(),av3=numeric(),av4=numeric(),av5=numeric(),act_id=numeric(),person_id=numeric(),axis_id=character())
  centroid_df<-as.numeric()
  for(i in c('x','y','z')){
    for(j in 1:15){
      for(k in 1:7){
        filter<-((df$axis_flag==i)&(df$person_flag==j)&(df$act_flag==k))
        temp<-c(av1=mean(v1[filter]),av2=mean(v2[filter]),av3=mean(v3[filter]),av4=mean(v4[filter]),av5=mean(v5[filter]),act_id=k,person_id=j,axis_id=i)
        #print(temp)
        centroid_df<-rbind(centroid_df,temp)
        #centroid_df<-rbind(centroid_df,temp)
      }
      
    }
    
  }
  
  centroid_df<-as.data.frame(centroid_df)
  
  #return(centroid_df)
  
  #per person per axis
  per_person<-numeric()
  for(i in c('x','y','z')){
    for(j in 1:15){
      filter <- ((centroid_df$person_id==j)&(centroid_df$axis_id==i))
      temp<-get_farthest(centroid_df[filter,])
      per_person<-rbind(per_person,temp)
    }
    
  }
  
  print(per_person)
  
  #per activity per axis
  per_activity<-numeric()
  for(i in c('x','y','z')){
    for(j in 1:7){
      filter <- ((centroid_df$act_id==j)&(centroid_df$axis_id==i))
      temp<-get_farthest(centroid_df[filter,])
      per_activity<-rbind(per_activity,temp)
    }
    
  }
  
  print(per_activity)
  
}