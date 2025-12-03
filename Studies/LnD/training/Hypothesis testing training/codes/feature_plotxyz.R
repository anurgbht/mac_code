feature_plotxyz<- function(act1,act2,interval_val,person_id){
  
  library(plotly)
  
  dfx<-feature_x(act1,act2,interval_val,person_id)
  dfy<-feature_y(act1,act2,interval_val,person_id)
  dfz<-feature_z(act1,act2,interval_val,person_id)
  dfn<-feature_n(act1,act2,interval_val,person_id)
  
  p <- subplot(
    plot_ly(x=dfx$valence1,y=dfx$valence2,mode='markers',color=dfx$act_flag),
    plot_ly(x=dfy$valence1,y=dfy$valence2,mode='markers',color=dfy$act_flag),
    plot_ly(x=dfz$valence1,y=dfz$valence2,mode='markers',color=dfz$act_flag),
    plot_ly(x=dfn$valence1,y=dfn$valence2,mode='markers',color=dfn$act_flag),
    
    margin = 0.05,
    nrows=2
  ) %>% layout(showlegend = FALSE)
  p
  
  
}