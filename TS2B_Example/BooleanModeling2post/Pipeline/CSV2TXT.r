####CSV to TXT-Parser####by Nina Kersten

#This R-Parser converts a .csv-file of a RPMA-Output to a .txt-file for inferring a boolean network with TS2B
#Up to 50 nodes can be calculated

#R version 3.4.3 (2017-11-30)
#install.packages("plyr")
#install.packages("dplyr")
#install.packages("stringr")
library(plyr)
#library(dplyr)
library(stringr)

homepath <- getwd()
if (!is.null(homepath)) setwd(homepath)
setwd(paste(homepath,"/CSV/",sep=""))

ldf <- list() # creates a list
celllinelist <- dir(pattern = "*_main.csv") # creates the list of all the csv files in the directory
for (k in 1:length(celllinelist)){
  ldf[[k]] <- read.csv(celllinelist[k])
}

#read-in the data, exlude SlideID, Antibody Name
for (d in celllinelist){
  newdata1 <- read.csv(file=paste(homepath,"/CSV/",d,sep = ""), header=FALSE, sep = ",", dec = ".", stringsAsFactors = FALSE)
  #celllinelist2 <- c("BT20", "BT549", "MCF7", "UACC812")
  newdata <-newdata1[!(newdata1$V4 == "Slide ID (1st chip)"),]
  newdata <-newdata[!(newdata$V4 == "HUGO ID"),]
  newdata<-newdata[!(newdata$V4 == "Slide ID (2nd chip)"),]
  newdata <-newdata[!(newdata$V4 == "Slide ID"),]
  newdata <-newdata[!(newdata$V4 == "Timepoint"),]
  #stimulilist<- c("Insulin", "IGF1", "FGF1", "EGF", "HGF" , "Serum", "NRG1" , "PBS") # List of all stimuli (pertubation parameter) used in the experiments in each cell line
  
  #for (i in stimulilist){
  
  #newdata2 <- subset(newdata, newdata$V4 == "0min" | newdata$V3 == i) # filter out the measurements of one cell line in combination with the 0-measurements and one of the pertubation parameters
  newdata2 <- newdata
  newdata3 <- newdata[1,]	
  newdata2 <- newdata2[, -c(1:3)]
  #newdata2 <- newdata2[,!(is.na(newdata2))]
  newdata2 <- newdata2[,colSums(is.na(newdata2))<nrow(newdata2)]
  newdata3 <- newdata3[, -c(1:3)]
  newdata3 <- newdata3[,!(is.na(newdata3))]
  newdata2 <- as.data.frame(sapply(newdata2,gsub,pattern="min",replacement=" "))
  newdata2 <- as.data.frame(sapply(newdata2,gsub,pattern="2hr",replacement="120"))
  newdata2 <- as.data.frame(sapply(newdata2,gsub,pattern="4hr",replacement="240"))
  #Combine the filtered dataset with the header of the antobodies names (names of the nodes in the network)
  newdata4 <- rbind(newdata3, newdata2) 
  newdata4[newdata4 == "Antibody Name"] = "#NON"
  split_newdata4 <- newdata4
  #split_newdata4 <- newdata4[,20]# Working with a smaller dataset
  e <- c("$", as.character("%"),"+", "-", ".","0","1","2","3","4","5","6","7","8","9", ":", ";","<",">","?", "@","A","B","C","D","E","F","G","H","I","J","K", "L", "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","_","`","~") #All possible single characters working with the TS2B model
  g <- c("NON", e[1:ncol(split_newdata4)-1])
  #g <- c(i, "NON", e[1:ncol(split_newdata4)-1])# Control: Shows wether the loop works by putting (i) in the headerof the .txt-file
  b <- (paste(g, collapse =" "))
  c <- as.data.frame(b)
  f <- rbind.fill(list(c,split_newdata4))
  f[1,2] <- as.character(f[1,1])
  f$b <- NULL
  f[is.na(f)] <- ""
  #delete doubled data
  f <- unique(f)
  
  
  
  #ifelse(!dir.exists("CSV2TXTOutput"), dir.create("CSV2TXTOutput"), "Folder exists already") # Creates a folder for the output
  newd <- str_replace(d, ".csv", "")
  write.table(f,paste(homepath,"/CSV2TXT_output/",newd,sep = "",".txt"), sep="\t", quote = FALSE, row.names=FALSE, col.names = FALSE)
  
  #}
}


