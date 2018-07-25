####CSV to TXT-Parser####by Nina Kersten

#This R-Parser converts a .csv-file of a RPMA-Output to a .txt-file for inferring a boolean network with TS2B
#Up to 48 nodes can be calculated

#install.packages("plyr")
#install.packages("data.table") #data.table_1.9.5
library(plyr)
library(data.table) 

setwd("/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/examples/")

### Creating the 1. Stimuli-Dataset: "FGF1"###

#read-in the data, exlude SlideID, Antibody Name
newdata <- read.csv(file="/home/nina/Schreibtisch/Masterarbeit/DREAM8-Breast-Cancer/Training data/experimental/experimental/CSV/BT549_main.csv", header=FALSE, skip = 2, sep = ",", dec = ".", stringsAsFactors = FALSE)
stimulilist<-c("Insulin", "IGF1", "EGF", "HGF" , "Serum", "NRG1" , "PBS")

  for (i in stimulilist){
    
      newdata2 <- subset(newdata, newdata$V4 == "0min" | newdata$V3 == stimulilist)
      #newdata2 <- subset(newdata, V4 == "0min" | V3 == "Insulin")
      newdata3 <- newdata[1,]	
      newdata2$V1 <- NULL
      newdata2$V2 <- NULL
      newdata2$V3 <- NULL
      newdata3$V1 <- NULL
      newdata3$V2 <- NULL
      newdata3$V3 <- NULL
      newdata2 <- as.data.frame(sapply(newdata2,gsub,pattern="min",replacement=" "))
      newdata2 <- as.data.frame(sapply(newdata2,gsub,pattern="2hr",replacement="120"))
      newdata2 <- as.data.frame(sapply(newdata2,gsub,pattern="4hr",replacement="240"))
      newdata4 <- rbind(newdata3, newdata2) 
      newdata4[newdata4 == "HUGO ID"] = "#NON"
      split_newdata4 <- newdata4# mit normaler Datensatzgröße weiterabeiten
      e <- c("!", "$", as.character("%"),"+", "-", ".","0","1","2","3","4","5","6","7","8","9", ":", ";", "?", "@","A","B","C","D","E","F","G","H","I","J","K", "L", "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z", "_", "~")
      g <- c("NON", e[1:ncol(split_newdata4)-1])
      b <- (paste(g, collapse =" "))
      c <- as.data.frame(b)
      f <- rbind.fill(list(c,split_newdata4))
      f[1,2] <- as.character(f[1,1])
      f$b <- NULL
      f[is.na(f)] <- ""
      
      #h <- f[with(f, order(V4)),] #Sort the measurements by the time

      write.table(f, file = paste(i,".txt"), quote = FALSE, row.names=FALSE, col.names = FALSE)

 
}
