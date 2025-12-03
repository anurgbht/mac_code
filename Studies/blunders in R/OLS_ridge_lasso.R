# we try to learn what OLS is, how it functions when the x's are highly correlated
# and how lasso and ridge take care of that

# our base equation is y = 2.7 + 2.9x1 + 7x2 + 9x3 + 6x4

# building training data

x1<-rnorm(2000,mean = 1,sd = 7)
x2<-rnorm(2000)
#x3<-x2+1+rnorm(2000)
x3<-x2+rnorm(2000)
x4<-runif(2000,min=-1,max=1)

data <- as.data.frame(cbind(x1,x2,x3,x4))

# checking to see if x2 x3 are indeed correlated or not
cor(data)

index<-1:2000
temp<-sample(index,1400,replace = FALSE)
train<-data[temp,]
test<-data[!index%in%temp,]

# getting the reference values
ytrain <- 2.7 + 2.9*train$x1 + 7*train$x2 + 9*train$x3 + 6*train$x4
ytest <- 2.7 + 2.9*test$x1 + 7*test$x2 + 9*test$x3 + 6*test$x4

train$y<-ytrain

# fitting the linear model on the train data

lm.fit <- lm(y~., data=train)
summary(lm.fit)

# Predicted data from lm
pr.lm <- predict(lm.fit,test)

plot(pr.lm,ytest)

