setwd('D:\\Confidential\\Projects\\Steel Research')

library('poLCA')
library('mclust')
dat<-read.csv('meanval_data.csv',sep='|')
dat<-dat[,-1]
mod_dat<-dat[,-7]

# dat$amplitude<-dat$amplitude - min(dat$amplitude) + 1
# dat$rms<-dat$rms - min(dat$rms) + 1
# dat$skew<-dat$skew - min(dat$skew) + 1
# dat$kurt<-dat$kurt - min(dat$kurt) + 1
# dat$var<-dat$var - min(dat$var) + 1
# dat$ekurt<-dat$ekurt - min(dat$ekurt) + 1

form<-cbind(amplitude,rms,skew,kurt,ekurt,var)~1

model<-poLCA(form,dat,nclass = 2)

# MCLUST based momdelling

class<-dat$label
table(class)

clPairs(mod_dat,class)
mc<-Mclust(mod_dat)
summary(mc)