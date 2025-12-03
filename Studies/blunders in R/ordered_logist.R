# Examples of ordered logistic regression

require(foreign)
require(ggplot2)
require(MASS)
require(Hmisc)
require(reshape2)

dat <- read.dta("http://www.ats.ucla.edu/stat/data/ologit.dta")
head(dat)

## one at a time, table apply, pared, and public
lapply(dat[, c("apply", "pared", "public")], table)

## three way cross tabs (xtabs) and flatten the table
ftable(xtabs(~ public + apply + pared, data = dat))


# box plot of all the variables
ggplot(dat, aes(x = apply, y = gpa)) +
  geom_boxplot(size = .75) +
  geom_jitter(alpha = .5) +
  facet_grid(pared ~ public, margins = TRUE) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1))

## fit ordered logit model and store results 'm'
m <- polr(apply ~ pared + public + gpa, data = dat, Hess=TRUE)

## view a summary of the model
summary(m)

# calculating the p values
## store table
(ctable <- coef(summary(m)))

## calculate and store p values
p <- pnorm(abs(ctable[, "t value"]), lower.tail = FALSE) * 2

## combined table
(ctable <- cbind(ctable, "p value" = p))

