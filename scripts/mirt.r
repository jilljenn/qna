library(CDM)
library(mirt)

train <- read.csv('icml/trainr.csv', header=FALSE)
test <- read.csv('icml/testr.csv', header=FALSE)

data = fraction.subtraction.data
qmatrix = as.matrix(fraction.subtraction.qmatrix)
# data = read.csv('data/banach.csv')
# qmatrix = as.matrix(read.csv('data/qmatrix-banach.csv'))

model = mirt.model(qmatrix)
d = dim(qmatrix)[2]
fit = mirt(data, model)
# d = 2
# fit = mirt(data, d)

computeError <- function(fit) {
    V <- coef(fit, simplify=TRUE)$items[,1:(d + 1)]
    U <- cbind(fscores(fit, method='MAP', full.scores=TRUE), rep(1))
    Z <- U %*% t(V)
    p <- 1 / (1 + exp(-Z))

    pred <- p[!is.na(test)]
    vrai <- test[!is.na(test)]

    log(1 - abs(pred - vrai), 2)

    print(p[1:5,])
    print(data[1:5,])
    print(colSums(abs(data - round(p)), 2))  # 8232 pour la connerie d = 2, 597 pour l'autre
    # Item.1 Item.2 Item.3 Item.4 Item.5 Item.6 Item.7 
    #    91     49    195    181      0      0     81 
    -colMeans(log(1 - abs(data - p), 2))
    #    Item.1    Item.2    Item.3    Item.4    Item.5    Item.6    Item.7 
    # 0.1581613 0.1444462 0.2427834 0.1972578 0.7838758 0.7948119 0.2195983 
}

d = 2
fit = mirt(data, d)
computeError(fit)

library(mirtCAT)
data2 <- data
data2[is.na(data2)] <- 0

CATdesign <- mirtCAT(NULL, fit, criteria='Drule', start_item='Drule', local_pattern=data2, design_elements=TRUE)

nextItem <- findNextItem(CATdesign)
print(nextItem)
summary(data[nextItem])

reply <- function(q, r) {
    CATdesign <- updateDesign(CATdesign, items=c(q), response=c(r))
    CATdesign$design@Update.thetas(CATdesign$design, CATdesign$person, CATdesign$test)
    nextItem <- findNextItem(CATdesign)
    print(nextItem)
    print(summary(data[nextItem]))
    print('rep.')
    print(data[1373, nextItem])
    nextItem
}

auto <- function(r) {
    reply(nextItem, r)
}

nextItem <- auto(0)
nextItem <- auto(1)

CATdesign <- updateDesign(CATdesign, items=c(68), response=c(1))
CATdesign$person$Update.thetas(CATdesign$design, CATdesign$test)
CATdesign$person$thetas

theta <- cbind(CATdesign$person$thetas, 1)
Z <- theta %*% t(V)
p <- 1 / (1 + exp(-Z))

nextItem <- findNextItem(CATdesign)
nextItem
summary(data[nextItem])

CATdesign <- updateDesign(CATdesign, items=c(68, 8), response=c(1, 0))
CATdesign$person$Update.thetas(CATdesign$design, CATdesign$test)
CATdesign$person$thetas

theta <- cbind(CATdesign$person$thetas, 1)
Z <- theta %*% t(V)
p <- 1 / (1 + exp(-Z))
ranked <- sort(p, index.return=TRUE)
p[,ranked$ix]

nextItem <- findNextItem(CATdesign)
nextItem
summary(data[nextItem])

CATdesign <- updateDesign(CATdesign, items=c(68, 8, 94), response=c(1, 0, 1))
CATdesign$person$Update.thetas(CATdesign$design, CATdesign$test)
CATdesign$person$thetas

theta <- cbind(CATdesign$person$thetas, 1)
Z <- theta %*% V
p <- 1 / (1 + exp(-Z))
ranked <- sort(p, index.return=TRUE)
ranked
p[,ranked$ix]

nextItem <- findNextItem(CATdesign)
nextItem
summary(data[nextItem])

CATdesign <- updateDesign(CATdesign, items=c(68, 8, 94, 129), response=c(1, 0, 1, 1))
CATdesign$person$Update.thetas(CATdesign$design, CATdesign$test)
CATdesign$person$thetas

theta <- cbind(CATdesign$person$thetas, 1)
Z <- theta %*% t(V)
p <- 1 / (1 + exp(-Z))
ranked <- sort(p, index.return=TRUE)
ranked
p[,ranked$ix]

write.csv(U, 'u.csv')
write.csv(V, 'v.csv')

write.csv(CATdesign$person$thetas_history, 'testlog.csv')
