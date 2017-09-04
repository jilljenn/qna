list.of.packages <- c("ltm", "catR", "CDM", "mirt", "mirtCAT")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages, repos='https://cran.ism.ac.jp/')
