library(ltm)
library(catR)

model = rasch(LSAT)
coeff = coef(model)
one = rep(1, 5)
itembank = cbind(coeff[,2:1], 1 - one, one)
theta = 0
scores = factor.scores(model, resp.patterns=LSAT)

nextItem(itembank, NULL, theta, criterion="MFI")
