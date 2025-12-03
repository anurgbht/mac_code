plotting_sub<-function(act_id,person_id){
  library('plotly')
  
  load('assdata.RData')
  
  #plot_ly(x=valence22,type='histogram')
  
  # p <- subplot(
  #   plot_ly(x=dfx$valence1,y=dfx$valence2,mode='markers',color=dfx$act_flag),
  #   plot_ly(x=dfy$valence1,y=dfy$valence2,mode='markers',color=dfy$act_flag),
  #   plot_ly(x=dfz$valence1,y=dfz$valence2,mode='markers',color=dfz$act_flag),
  #   plot_ly(x=dfn$valence1,y=dfn$valence2,mode='markers',color=dfn$act_flag),
  #   
  #   margin = 0.05,
  #   nrows=2
  # ) %>% layout(showlegend = FALSE)
  # p
  
  #plot_ly(x=dfx$valence1,y=dfx$valence2,mode='markers',color=dfx$act_flag)
  
  # dat1<-df$valence2[(df$act_flag==act_id)&(df$person_flag==person_id)]
  # dat2<-df$valence5[(df$act_flag==act_id)&(df$person_flag==person_id)]
  # 
  # coldat<-df$axis_flag[(df$act_flag==act_id)&(df$person_flag==person_id)]
  # plot_ly(x=dat1,y=dat2,mode='markers',color = coldat)

  ###############################################
  
  # act_id<-4
  
  dat1<-df$valence2[(df$act_flag==act_id)&(df$axis_flag==person_id)]
  dat2<-df$valence5[(df$act_flag==act_id)&(df$axis_flag==person_id)]
  
  coldat<-df$person_flag[(df$act_flag==act_id)&(df$axis_flag=='x')]
  plot_ly(x=dat1,y=dat2,mode='markers',color = coldat)
  
  
}