#!/usr/bin/env Rscript

#R version 3.4.3 (2017-11-30)
#install.packages("plyr")
#install.packages("stringr")
library(plyr)
library(stringr)

#args = commandArgs(trailingOnly=TRUE)
args <- "./CSV_insilico/Gold_mybnet.csv"
args1 <- gsub('./CSV_insilico/Gold_mybnet.csv','CSV_insilico/Gold_mybnet.csv',args)
#if (!is.null(homepath)){
#  setwd(homepath)
#  }
#print(homepath)

#incoming argument: './CSV_insilico/*.csv'
homepath <- getwd()
pathname <- file.path(homepath,"Pipeline_insilico/PyBoolNet/",args1)

#ldf <- list() # creates a list
#celllinelist <- dir(homepath1, pattern = "/Gold_*.csv") # creates the list of all the csv files in the directory
#print(celllinelist)
#for (k in 1:length(celllinelist)){
#  ldf[[k]] <- read.csv(celllinelist[k])
#}
#print(celllinelist)


#read-in the data, exlude SlideID, Antibody Name
#for (d in celllinelist){
  newdata1 <- read.csv(file=pathname, header=FALSE, sep = ",", dec = ".", stringsAsFactors = FALSE)
  #celllinelist2 <- c("BT20", "BT549", "MCF7", "UACC812")
  newdata <-newdata1[!(newdata1$V4 == "Slide ID (1st chip)"),]
  newdata <-newdata[!(newdata$V4 == "HUGO ID"),]
  newdata<-newdata[!(newdata$V4 == "Slide ID (2nd chip)"),]
  newdata <-newdata[!(newdata$V4 == "Slide ID"),]
  #stimulilist<- c("Insulin", "IGF1", "FGF1", "EGF", "HGF" , "Serum", "NRG1" , "PBS") # List of all stimuli (pertubation parameter) used in the experiments in each cell line
  stimulilist<- c("Insulin") # List of all stimuli (pertubation parameter) used in the experiments in each cell line
  
  for (i in stimulilist){
    
    newdata2 <- subset(newdata, newdata$V4 == "0min" | newdata$V3 == i) # filter out the measurements of one cell line in combination with the 0-measurements and one of the pertubation parameters
    newdata3 <- newdata[1,]	
    newdata2 <- newdata2[, -c(1:3)]
    newdata3 <- newdata3[, -c(1:3)]
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
    
    
    
    #ifelse(!dir.exists("CSV2TXTOutput"), dir.create("CSV2TXTOutput"), "Folder exists already") # Creates a folder for the output
    newd <- str_replace(args1, ".csv", "")
    newd1 <- str_replace(newd, "CSV_insilico/","")
    outputpath <- file.path(homepath,"Pipeline_insilico/PyBoolNet/CSV_insilico_2_TXT/")
    write.table(f,paste(outputpath, newd1,i,sep = "",".txt"), sep="\t", quote = FALSE, row.names=FALSE, col.names = FALSE)
    
  }
#}


