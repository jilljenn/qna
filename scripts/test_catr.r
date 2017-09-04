library(ltm)
library(catR)

coeff <- coef(rasch(LSAT))
one <- rep(1, 5)
itembank <- cbind(coeff[,2:1], 1 - one, one)

nextItem(itembank, NULL, theta, criterion="MFI")
