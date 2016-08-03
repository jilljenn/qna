library(CDM)
library(mirt)

# data = fraction.subtraction.data
# qmatrix = fraction.subtraction.qmatrix
data = read.csv('data/banach.csv')
qmatrix = as.matrix(read.csv('data/qmatrix-banach.csv'))

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

CATdesign <- mirtCAT(NULL, fit, criteria='Drule', start_item='Drule', local_pattern=data, design_elements=TRUE)
mirtCAT.findNextItem(CATdesign)
CATdesign <- updateDesign(CATdesign, items=c(6), response=c(0))
CATdesign$person$Update.thetas(CATdesign$design, CATdesign$test)
CATdesign$person$thetas
